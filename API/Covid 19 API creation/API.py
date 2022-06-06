import bs4 as bs 
import requests 
import numpy as np
import os 
import pandas as pd 
import pandas_datareader.data as web 
import datetime as dt 
from datetime import datetime
from datetime import date, timedelta
import glob
import json
import openpyxl
import mysql.connector
from sqlalchemy import create_engine
import pymysql
import pymysql
import numpy as np
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import cryptography
import password_configuration_Ori




#--------------------------------------------------------------- ETL ------------------------------------------------------------------

#I define the list of countries that I will be using for this case.
Initial_list_of_countries= ["austria", "belgium", "bulgaria", "croatia", "denmark", "estonia", "finland", "france", "germany", "greece", "hungary", "ireland", "italy", "latvia", "lithuania", "luxembourg", "malta", "netherlands", "poland", "portugal", "romania", "slovakia", "slovenia", "spain"]
# To try the recall functionality I will leave Spain out of the list.

#I define the dates that I will use as "starting date" and "end date" for the API.
Initial_date_selection_1="2020-03-20"
Initial_date_selection_2="2020-03-22"



#------------------------------------------------------------ EXTRACTION ------------------------------------------------------------------



def Extract(List_of_countries,date_selection_1,date_selection_2): 
    print("\n"*2)
    print("Selected date (from): ",date_selection_1)
    print("Selected date (until): ",date_selection_2)
    print("")
    
    data_final=pd.DataFrame()
    #For every country in the "List_of_countries" that we have defined this loops iterates to get all the data. 
    for id,country_identification in enumerate(List_of_countries):
        print("Country: ",country_identification.capitalize())

        #The following link is the API and it has 3 empty spaces that will be fullfilled with the country that is assigned to every iteration and with the "Starting" and "end" dates.
        resp=requests.get("https://api.covid19tracking.narrativa.com/api/country/{}?date_from={}&date_to={}".format(country_identification,date_selection_1,date_selection_2))
        JSON_COMPLETE=resp.json()['dates'] #we get all the data in JSON format. The key of every json dictionary is the date.
        
        for data in JSON_COMPLETE:#with this forloop I open the different dictionaries. 
        #this dictionaries contain other dictionaries that have as key the word "countries" 
        
            
            data_JSON=JSON_COMPLETE['{}'.format(data)]
            
            country=data_JSON["countries"]
     
         
           #when I open the "countries" key then  I find the name of the country for example "Sweden". 
           #and thus I need to open for every existing country.
           #Here I found a problem, because not all the countries had data divided by Region and thus, using a "if" 
           #I separate between these 2 types of countries. 
           #if the list under the key "Region" had no elements (so the length of the list is 0), then I was getting 
           #all the existing data in the current point, if by contrary the country HAS data by region, then we will keep on digging.
           
            if len(country['{}'.format(country_identification.capitalize())]['regions']) == 0: #if there are no elements in the list "Regions"
                
                #Then open the json under the key of the name of the country
                JSON_FINAL=country['{}'.format(country_identification.capitalize())]
                #transpose the json (so it is in the right format to build a dataset)
                data_temp=pd.DataFrame(JSON_FINAL.items()).transpose()#get the data in a dataframe format and transpose it to get the result I want.
                
                #since the result of the last operation give us two lines one of them being the headers, we transform the first row into headers and delete the first row 
                data_temp.columns = data_temp.iloc[0] #the first row as a header
                data_temp = data_temp.iloc[1: , :] #I delete the first row (because it was the header)
                #we also include in the dataset one column to show the name of the country from which the data is comming  
                data_temp=data_temp.drop(["name"],axis=1)
                data_temp['Country']=country_identification.capitalize()
                
                data_final=pd.concat([data_final,data_temp]) #aconcatenate the two dataframes
                
            #if by the contrary, the Json contains data in the "region" key, then we procrede doing the following    
            else : 
                for id,elements in enumerate(country['{}'.format(country_identification.capitalize())]['regions']): 
                    Region_Name=elements['name'] #first we get the name of the region
            
                    if len(elements['sub_regions']) == 0: #then we check if the region also has subregions or not
                    #if it doesn't then we do the same that we did with the "regions" we get the data that we have in this case, 
                    #inside of the "Regions" dictionary
           
                       data_temp=pd.DataFrame(elements.items()).transpose()#get the data in a dataframe format and transpose it to get the result I want.
                       data_temp.columns = data_temp.iloc[0] #the first row as a header
                       data_temp = data_temp.iloc[1: , :] #I delete the first row (because it was the header)
                       data_temp=data_temp.drop(["name"],axis=1)
                       data_temp["Region_Name"]=Region_Name #add the column "country_name"
                       data_temp['Country']=country_identification.capitalize()
                       data_final=pd.concat([data_final,data_temp]) #aconcatenate the two dataframes
                 
                    else: #If the country do contain sub_regions, then for every element in the subregion 
                    #we get the data. 
                        for id,subregion in enumerate(elements['sub_regions']):
                            
                            data_temp=pd.DataFrame(subregion.items()).transpose()#get the data in a dataframe format and transpose it to get the result I want.
                            data_temp.columns = data_temp.iloc[0] #the first row as a header
                            data_temp = data_temp.iloc[1: , :] #I delete the first row (because it was the header)
                            data_temp["Region_Name"]=Region_Name #add the column "country_name"
                            data_temp['Country']=country_identification.capitalize()
                            data_final=pd.concat([data_final,data_temp]) #aconcatenate the two dataframes
    print("\n"*2)  
    print("Data at the end of the Extraction: ", data_final.columns)   
    print("\n"*2)            
    return (data_final)   
        


#------------------------------------------------------------ TRANSFORMATION ------------------------------------------------------------------



def Transform(List_of_countries,date_selection_1,date_selection_2):
    
    data_final=Extract(List_of_countries,date_selection_1,date_selection_2)
    data_final.rename(columns = {'name':'City_Name'}, inplace = True)
    #Since the "nan" value" can give us problems, we replace them with Nones 
    data_final=data_final.replace({np.nan: None})
    
    #In the dataset we have plenty of columns that won't be useful and thus we can delete them. 
    #in this case, since I want to automatize the upload to the MySQL and thus I need to have all the data standarized
    #meaning that all the dataframes should have the same columns, since this cannot be guaranteed with the data that we get from the API 
    #(for example, if just Bulgaria is called, it doesn't have "sub_regions")
    #In order to standarize everything, before deleting the columns that we don't want
    #in case that the API gives us data that misses any of the columns that we want, 
    #we will add it. 
    
    
    #we start this process, by defining the names of the columns that we want.
    Columns_that_I_want_to_keep=['date','City_Name', 'source', 'today_confirmed', 'today_deaths', 'today_open_cases',  'today_recovered', 'today_vs_yesterday_confirmed', 'today_vs_yesterday_deaths', 'today_vs_yesterday_open_cases', 'today_vs_yesterday_recovered', 'Country', 'sub_regions', 'Region_Name' , 'today_intensive_care', 'today_total_hospitalised_patients', 'today_vs_yesterday_intensive_care', 'today_vs_yesterday_total_hospitalised_patients', 'today_home_confinement', 'today_hospitalised_patients_with_symptoms','today_tests', 'today_vs_yesterday_home_confinement','today_vs_yesterday_hospitalised_patients_with_symptoms', 'today_vs_yesterday_tests']
    
    #then, we check from the columns that we want, which ones are not present in the list of names of the columns of our "data_final" dataframe
    list_difference = [item for item in Columns_that_I_want_to_keep if item not in data_final.columns]
    
    #now, for every missing column, we will create it in the "data_final" dataset with None values.
    for index,element in enumerate(list_difference): 
        data_final['{}'.format(element)]=None
        
    
    #Finally, we define the columns that we want to keep, all the rest are dropped.
    data_final=data_final[['date','City_Name', 'source', 'today_confirmed', 'today_deaths', 'today_open_cases',  'today_recovered', 'today_vs_yesterday_confirmed', 'today_vs_yesterday_deaths', 'today_vs_yesterday_open_cases', 'today_vs_yesterday_recovered', 'Country',  'Region_Name' , 'today_intensive_care', 'today_total_hospitalised_patients', 'today_vs_yesterday_intensive_care', 'today_vs_yesterday_total_hospitalised_patients', 'today_home_confinement', 'today_hospitalised_patients_with_symptoms','today_tests', 'today_vs_yesterday_home_confinement','today_vs_yesterday_hospitalised_patients_with_symptoms', 'today_vs_yesterday_tests']]
    #data_final=data_final.drop(['name_es', 'name_it','yesterday_recovered','yesterday_intensive_care', 'yesterday_total_hospitalised_patients','yesterday_confirmed', 'yesterday_deaths',],axis=1)
    
    #Now we we reorder the columns so the categories are in the left part of the table and the measures in the right part. 
    
    data_final = data_final.reindex(columns=['date','City_Name', 'source', 'Country', 'Region_Name', 'today_confirmed', 'today_deaths', 'today_open_cases',  'today_recovered', 'today_intensive_care', 'today_total_hospitalised_patients', 'today_home_confinement', 'today_tests','today_vs_yesterday_confirmed', 'today_vs_yesterday_deaths', 'today_vs_yesterday_open_cases', 'today_vs_yesterday_recovered',  'today_vs_yesterday_intensive_care', 'today_vs_yesterday_total_hospitalised_patients', 'today_hospitalised_patients_with_symptoms','today_vs_yesterday_home_confinement','today_vs_yesterday_hospitalised_patients_with_symptoms', 'today_vs_yesterday_tests'])
    
    data_final['new_cases_minus_new_recoveries']=data_final['today_confirmed']-data_final['today_recovered']
    #just  in case new nans have been created in the process we substitute them again with None.
    data_final=data_final.replace({np.nan: None})
    
    return (data_final) 



#------------------------------------------------------------------ LOAD ------------------------------------------------------------------



def Load(List_of_countries,date_selection_1,date_selection_2,The_function_has_been_initiated_from_any_of_the_API_endpoinds):
    
    data_final=Transform(List_of_countries,date_selection_1,date_selection_2)
    #We start creating the connection that will enable us to work in MySQL using python.
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password=password_configuration_Ori.password,
                                 db='test2')
    #We then define the cursor since this is the basic element that we need to move inside the database.
    cursor=connection.cursor()
    
    #This part of the "Load" function will reestart the database if needed. 
    #the varaible "The_function_has_been_initiated_from_any_of_the_API_endpoinds" will be set as "True" if the "Load" function
    #has been called from any of the API endpoints, otherwhise it will be false. 
    #The pupose of this is to allow the MySQL table to get reset the code but not when my API gets new data from the source API.
    if The_function_has_been_initiated_from_any_of_the_API_endpoinds == False:
        cursor.execute("DROP table Test_table")
        cursor.execute("CREATE table Test_table(ID_Register INT AUTO_INCREMENT PRIMARY KEY, date_register DATE, City_Name VARCHAR(100),source VARCHAR(100),  Country_name VARCHAR(100), Region_name VARCHAR(100),            today_confirmed INT,today_deaths INT, today_open_cases INT, today_recovered INT,  today_intensive_care INT,    today_total_hospitalised_patients INT, today_home_confinement INT,   today_tests INT,             today_vs_yesterday_confirmed DECIMAL(4,2), today_vs_yesterday_deaths DECIMAL(4,2), today_vs_yesterday_open_cases DECIMAL(4,2), today_vs_yesterday_recovered DECIMAL(6,2),      today_vs_yesterday_intensive_care DECIMAL(4,2), today_vs_yesterday_total_hospitalised_patients DECIMAL(4,2),  today_hospitalised_patients_with_symptoms INT,  today_vs_yesterday_home_confinement DECIMAL(4,2), today_vs_yesterday_hospitalised_patients_with_symptoms DECIMAL(4,2), today_vs_yesterday_tests DECIMAL(4,2), new_cases_minus_new_recoveries INT) ")

    #This line of code will define which fields we will fullfill with the data that we will send in the next lines.                               
    sql = "INSERT INTO Test_table (date_register,  City_Name, source, Country_name ,  Region_name, today_confirmed ,today_deaths , today_open_cases , today_recovered ,   today_intensive_care ,   today_total_hospitalised_patients , today_home_confinement ,  today_tests ,  today_vs_yesterday_confirmed, today_vs_yesterday_deaths , today_vs_yesterday_open_cases , today_vs_yesterday_recovered, today_vs_yesterday_intensive_care , today_vs_yesterday_total_hospitalised_patients ,  today_hospitalised_patients_with_symptoms, today_vs_yesterday_home_confinement , today_vs_yesterday_hospitalised_patients_with_symptoms , today_vs_yesterday_tests, new_cases_minus_new_recoveries  ) VALUES (%s,%s,%s,    %s,%s,%s,    %s,%s,%s,     %s,%s,%s,         %s,%s,%s,        %s,%s,%s,       %s,%s,%s,      %s,%s,%s)"

    #this for loop will get all the dataframe "data_final" and for every row divide the elements so they can be introduced in MYSQL.
    for index in range(0,len(data_final)):                 
        data=list(data_final.iloc[index])
        # Execute the query
        cursor.execute(sql, (data[0],data[1],data[2],data[3],data[4],data[5], data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13],data[14], data[15],data[16],data[17], data[18],data[19],data[20], data[21],data[22],data[23]))
        connection.commit()
        
    return(data_final)


    




#----------------------------------------------------- INITIALIZE THE FUNCTIONS --------------------------------------------------------

#Here is where I will initialize the "load" function, since it is not being initialized from any of my API endpoints, then 
#the variable "The_function_has_been_initiated_from_any_of_the_API_endpoinds" will be false.
The_function_has_been_initiated_from_any_of_the_API_endpoinds=False
data_final=Load(Initial_list_of_countries,Initial_date_selection_1,Initial_date_selection_2,The_function_has_been_initiated_from_any_of_the_API_endpoinds)
#NOW THE DATA IS ALREADY IN OUR DATABASE



#------------------------------------------------------------------ API ------------------------------------------------------------------

#Here we start defining the connector and cursor, because since the other connector and cursor that we defined are in the "Load we cannot use them outside. 
connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password=password_configuration_Ori.password,
                                 db='test2')
    #We then define the cursor since this is the basic element that we need to move inside the database.
cursor=connection.cursor()



#We start the creation of the API by creating the app and the API.
app = Flask(__name__)
api = Api(app)


#All the APIS are build in a similar way and thus I will just be commenting the first one

#I start defining the class that will inherit its functionalities from the "Resource" library
class Country(Resource):
    #then I define a function, in this case, this function will receive the "Country" as a variable. 
    #The "self" is here, because we are defining a class, however all the other methods, for exampe the "__init__" are already 
    #defined in the "Resource" library . 
    
    #The variable "Country" is defined in the following line of code "api.add_resource(Country, '/items/<string:Country>')"
    #where I say that the user, to acces the Country endpoint, will need to specify the root (http://127.0.0.1:???) (the ??? are the port that I will define with the code "app.run(port=111)" currently is 111. )
    #and the endpoint "/items/<string:Country>" being the "Country" the country that the user wants.  
    def get(self, Country):
        
        #I have build the code in a way that if the user makes a query and the data that he/she is asking is not in the database, 
        #The code calls the function "load" that will activate the other functions so we can obtain from the source API 
        #the registers that will go trough the ETL process and saved in our database, then delivered to the user that is making the query
        
        datos=pd.read_sql('SELECT * FROM Test_table WHERE Country_name = "{}"'.format(Country.capitalize()), connection)
        
        
        #If the result of the query that we did to our database returns empty, then we procede with this code
        if datos.empty:
            print("")
            #first we define the dates, in this case, since in the "Country" class we don't ask for any date, 
            #we will get the existing data from (current date -3 days ) until (current date)
            current_date=date.today()
            delta = timedelta(3)
            current_date_minuts_3_days=current_date-delta
            
            #Then we print the following sentence so we keep a log
            print('DataFrame is empty! getting new data for {} between the dates {} and {}'.format(Country.capitalize(),current_date_minuts_3_days,current_date))
            
            #Then we put the country selected in a list. 
            country_selected=[]
            country_selected.append(Country)
            
            #We set the variable "The_function_has_been_initiated_from_any_of_the_API_endpoinds" as True, because 
            #in this case the "load" function has been called from an endpoint (the Country endpoint)
            The_function_has_been_initiated_from_any_of_the_API_endpoinds=True
            #and then we call the "Load funtion"
            Load(country_selected,current_date_minuts_3_days,current_date,The_function_has_been_initiated_from_any_of_the_API_endpoinds)
            #We comming the changes" and then create an other query agains our database. 
            connection.commit()
            datos=pd.read_sql('SELECT * FROM Test_table WHERE Country_name = "{}"'.format(Country.capitalize()), connection)
            
        json_datos = json.loads('{"items":' + datos.to_json(orient='records', date_format='iso') + '}')
        return (json_datos['items'])


class Region(Resource):

    def get(self, Country, Region):
        datos=pd.read_sql('SELECT * FROM Test_table WHERE Country_name = "{}" AND Region_name="{}"'.format(Country.capitalize(),Region.capitalize()), connection)
        
        if datos.empty:
            print("")
            current_date=date.today()
            delta = timedelta(3)
            current_date_minuts_3_days=current_date-delta
            print('DataFrame is empty! getting new data for {} between the dates {} and {}'.format(Country.capitalize(),current_date_minuts_3_days,current_date))
            country_selected=[]
            country_selected.append(Country)
            The_function_has_been_initiated_from_any_of_the_API_endpoinds=True
            Load(country_selected,current_date_minuts_3_days,current_date,The_function_has_been_initiated_from_any_of_the_API_endpoinds)
            connection.commit()
            datos=pd.read_sql('SELECT * FROM Test_table WHERE Country_name = "{}" AND Region_name="{}"'.format(Country.capitalize(),Region.capitalize()), connection)
               
        json_datos = json.loads('{"items":' + datos.to_json(orient='records', date_format='iso') + '}')
        return (json_datos['items'])


class City(Resource):

    def get(self, Country,Region, City):
        datos=pd.read_sql('SELECT * FROM Test_table WHERE Country_name = "{}" AND Region_name="{}" AND City_name="{}"'.format(Country.capitalize(),Region.capitalize(), City.capitalize()), connection)
        
        if datos.empty:
            print("")
            current_date=date.today()
            delta = timedelta(3)
            current_date_minuts_3_days=current_date-delta
            print('DataFrame is empty! getting new data for {} between the dates {} and {}'.format(Country.capitalize(),current_date_minuts_3_days,current_date))
            country_selected=[]
            country_selected.append(Country)
            The_function_has_been_initiated_from_any_of_the_API_endpoinds=True
            Load(country_selected,current_date_minuts_3_days,current_date,The_function_has_been_initiated_from_any_of_the_API_endpoinds)
            connection.commit()
            print('SELECT * FROM Test_table WHERE Country_name = "{}" AND Region_name="{}" AND City_name="{}"'.format(Country.capitalize(),Region.capitalize(), City.capitalize()))
            datos=pd.read_sql('SELECT * FROM Test_table WHERE Country_name = "{}" AND Region_name="{}" AND City_name="{}"'.format(Country.capitalize(),Region.capitalize(), City.capitalize()), connection)
            print(datos)
        
        json_datos = json.loads('{"items":' + datos.to_json(orient='records', date_format='iso') + '}')
        return (json_datos['items'])


class ItemList(Resource):
    def get(self):
        datos=pd.read_sql('SELECT * FROM Test_table', connection)
        json_datos = json.loads('{"items":' + datos.to_json(orient='records', date_format='iso') + '}')
        return (json_datos['items'])


class Date(Resource):
    def get(self, Date):
      
        datos=pd.read_sql('SELECT * FROM Test_table WHERE date_register=Date("{}")'.format(Date), connection)
        
        if datos.empty:
            print("")
            Selected_date=Date
            print('DataFrame is empty! geting data from all the countries for the date "{}"'.format(Selected_date))
            country_selected=[]
            for Country in Initial_list_of_countries:
                country_selected.append(Country)
                
            The_function_has_been_initiated_from_any_of_the_API_endpoinds=True
            Load(country_selected,Selected_date,Selected_date,The_function_has_been_initiated_from_any_of_the_API_endpoinds)
            connection.commit()
            datos=pd.read_sql('SELECT * FROM Test_table WHERE date_register=Date("{}")'.format(Date), connection)
            
        json_datos = json.loads('{"items":' + datos.to_json(orient='records', date_format='iso') + '}')
        return (json_datos['items'])
    
    
class Dates(Resource):
    def get(self, Date1, Date2):
    
        if Date1>Date2: 
            return ({"Answer": "The 'from' date should be earlier than the 'until' date"})
       
        datos=pd.read_sql('SELECT * FROM Test_table WHERE date_register BETWEEN Date("{}") AND Date("{}")'.format(Date1,Date2), connection)
        
        if datos.empty:
            print("")
            
            print('DataFrame is empty! geting data for all the countries from "{}" until "{}"'.format(Date1,Date2))
            country_selected=[]
            for Country in Initial_list_of_countries:
                country_selected.append(Country)
                
            The_function_has_been_initiated_from_any_of_the_API_endpoinds=True
            Load(country_selected,Date1,Date2,The_function_has_been_initiated_from_any_of_the_API_endpoinds)
            connection.commit()
            datos=pd.read_sql('SELECT * FROM Test_table WHERE date_register BETWEEN Date("{}") AND Date("{}")'.format(Date1,Date2), connection)
        
        json_datos = json.loads('{"items":' + datos.to_json(orient='records', date_format='iso') + '}')
        return (json_datos['items'])
    
    
class Country_Dates(Resource):
    def get(self, Country, Date1, Date2):
    
        if Date1>Date2: 
            return ({"Answer": "The 'from' date should be earlier than the 'until' date"})
       
        datos=pd.read_sql('SELECT * FROM Test_table WHERE (Country_name = "{}") AND (date_register BETWEEN Date("{}") AND Date("{}")) '.format(Country.capitalize(),Date1,Date2), connection)
        
        if datos.empty:
            print("")
            
            print('DataFrame is empty! geting data from "{}" from "{}" until "{}"'.format(Country.capitalize(),Date1,Date2))
            country_selected=[]
            country_selected.append(Country)
                
            The_function_has_been_initiated_from_any_of_the_API_endpoinds=True
            Load(country_selected,Date1,Date2,The_function_has_been_initiated_from_any_of_the_API_endpoinds)
            connection.commit()
            datos=pd.read_sql('SELECT * FROM Test_table WHERE (Country_name = "{}") AND (date_register BETWEEN Date("{}") AND Date("{}")) '.format(Country.capitalize(),Date1,Date2),connection)
        
        
        json_datos = json.loads('{"items":' + datos.to_json(orient='records', date_format='iso') + '}')
        return (json_datos['items'])





class avg_group_by_date(Resource):
    def get(self):
      
        datos=pd.read_sql('SELECT date_register, AVG(today_confirmed) AS today_confirmed , AVG(today_deaths) AS today_deaths, AVG(today_open_cases) AS today_open_cases,AVG(today_recovered) AS today_recovered,AVG(today_intensive_care) AS today_intensive_care,AVG(today_total_hospitalised_patients) AS today_total_hospitalised_patients,AVG(today_home_confinement) AS today_home_confinement, AVG(today_tests) AS today_tests FROM Test_table GROUP BY date_register', connection)
        json_datos = json.loads('{"items":' + datos.to_json(orient='records', date_format='iso') + '}')
        return (json_datos['items'])

class avg_group_by_Country(Resource):
    def get(self):
      
        datos=pd.read_sql('SELECT Country_name, AVG(today_confirmed) AS today_confirmed , AVG(today_deaths) AS today_deaths, AVG(today_open_cases) AS today_open_cases,AVG(today_recovered) AS today_recovered,AVG(today_intensive_care) AS today_intensive_care,AVG(today_total_hospitalised_patients) AS today_total_hospitalised_patients,AVG(today_home_confinement) AS today_home_confinement, AVG(today_tests) AS today_tests FROM Test_table GROUP BY Country_name', connection)
        json_datos = json.loads('{"items":' + datos.to_json(orient='records', date_format='iso') + '}')
        return (json_datos['items'])
    
class Country_and_date_that_have_the_higher_number_in_the_selected_measure(Resource):

    def get(self, measure):
      
        datos=pd.read_sql('SELECT Country_name, date_register, max({}) from Test_table WHERE today_confirmed= (SELECT  max({}) FROM Test_table)'.format(measure,measure),connection)
        json_datos = json.loads('{"items":' + datos.to_json(orient='records', date_format='iso') + '}')
        return (json_datos['items'])


class avg_group_by_Country_TOP_5_of_selected_measure(Resource):
    def get(self, measure):
      
        datos=pd.read_sql('SELECT Country_name, sum(today_confirmed) AS today_confirmed , sum(today_deaths) AS today_deaths, sum(today_open_cases) AS today_open_cases,sum(today_recovered) AS today_recovered,sum(today_intensive_care) AS today_intensive_care,sum(today_total_hospitalised_patients) AS today_total_hospitalised_patients,sum(today_home_confinement) AS today_home_confinement, sum(today_tests) AS today_tests FROM Test_table GROUP BY Country_name ORDER BY {} DESC LIMIT 5'.format(measure), connection)
        json_datos = json.loads('{"items":' + datos.to_json(orient='records', date_format='iso') + '}')
        return (json_datos['items'])



#this are the part where I relate the different classes with the different endpoint. 
#for example the class "Country" will be called every time that the user makes a query that includes 
#the localhost "http://127.0.0.1:???" (the ??? are the port that I will define with the code "app.run(port=111)" currently is 111. )
    #and the endpoint "/items/<string:Country>" being the "Country" the country that the user wants.  


#Categories
api.add_resource(ItemList, '/items')
api.add_resource(Country, '/items/<string:Country>')
api.add_resource(Region, '/items/<string:Country>/<string:Region>')
api.add_resource(City, '/items/<string:Country>/<string:Region>/<string:City>')
api.add_resource(Date, '/items/date/<string:Date>')
api.add_resource(Dates, '/items/dates/from/<string:Date1>/until/<string:Date2>')
api.add_resource(Country_Dates, '/items/<string:Country>/dates/from/<string:Date1>/until/<string:Date2>')

#Measures
api.add_resource(avg_group_by_date, '/measures/avg_date')
api.add_resource(avg_group_by_Country, '/measures/avg_country')
api.add_resource(Country_and_date_that_have_the_higher_number_in_the_selected_measure, '/measures/Max/<string:measure>')
api.add_resource(avg_group_by_Country_TOP_5_of_selected_measure, '/measures/TOP5/<string:measure>')


#This is the port that the API will be located in. 
app.run(port=223)



