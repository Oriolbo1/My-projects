# -*- coding: utf-8 -*-
"""
Created on Sun May  1 16:31:00 2022

@author: Oriol
"""


#The following code is a machine learning script that wouldbe running permanently and every workday
#would predict which departments would need data that day and which dates would they need. 
#The country that they will need data from depends on which country does every department works for. 

#As we will see in the code, the "department_1" works for Spain and normally retrieves data from 
#this country. 


#The following code, creates a Random dataset, I do that, because the API 
#is running on my computer and thus I cannot get real data from real users. 
#however, since I wanted to develop a machine learning program I needed some data. 

#The results of the machine learning models won't be accurated, since the random data 
#doesn't have patterns. It is not ideal, but at least we can see the process of creation 
#of the models. 



#IMPORTANT!

#I will start now creating the fake data. In a normal case, it wouldn't be needed. 
#you can skip the code untill seeing that I am starting to create the first neural netwrork. 


#HERE I START CREATING THE FAKE DATA
#[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[


import pandas as pd
import random
from faker import Faker
from random import randrange
from datetime import datetime
from datetime import datetime as date
import numpy as np

nr_of_customers = 5000
fake = Faker('de_DE')
customers = []

#I create this 2 lists because I will be using them in diferent points of the code. 
list_of_countries= ["Spain","Austria", "Belgium",  "Croatia", "Denmark", "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", "Ireland", "Italy", "Latvia", 
                    "Lithuania", "Luxembourg", "Malta", "Netherlands", "Poland", "Portugal", "Romania", "Slovakia", "Slovenia", "Sweden"]
list_of_departments=["department_1","department_2","department_3","department_4"]

#I start creating the Fake dataset --------------------------------------------------


for customers_id in range(nr_of_customers):
    

    d1 = datetime.strptime(f'1/1/2019', '%m/%d/%Y')
    d2 = datetime.strptime(f'1/1/2022', '%m/%d/%Y')
    Query_date = fake.date_between(d1, d2)
    date_name=Query_date.strftime("%A")


    User_identification = random.choice(["AAAAA@Zurich.com","BBBBB@Zurich.com","CCCCC@Zurich.com","DDDDD@Zurich.com","EEEEE@Zurich.com","FFFFF@Zurich.com",
                                         "GGGGG@Zurich.com","HHHHH@Zurich.com","IIIII@Zurich.com","JJJJJ@Zurich.com","KKKKK@Zurich.com","LLLLL@Zurich.com",
                                         "MMMMM@Zurich.com","NNNNN@Zurich.com","OOOOO@Zurich.com","PPPPP@Zurich.com","QQQQQ@Zurich.com","RRRRR@Zurich.com",
                                         "SSSSS@Zurich.com","TTTTT@Zurich.com","UUUUU@Zurich.com","VVVVVVV@Zurich.com","WWWWWW@Zurich.com","XXXXX@Zurich.com"])
    
    User_department_dictionary={"AAAAA@Zurich.com":"department_1","BBBBB@Zurich.com":"department_1","CCCCC@Zurich.com":"department_1","DDDDD@Zurich.com":"department_1","EEEEE@Zurich.com":"department_1","FFFFF@Zurich.com":"department_1",
                     "GGGGG@Zurich.com":"department_2","HHHHH@Zurich.com":"department_2","IIIII@Zurich.com":"department_2","JJJJJ@Zurich.com":"department_2","KKKKK@Zurich.com":"department_2","LLLLL@Zurich.com":"department_2",
                     "MMMMM@Zurich.com":"department_3","NNNNN@Zurich.com":"department_3","OOOOO@Zurich.com":"department_3","PPPPP@Zurich.com":"department_3","QQQQQ@Zurich.com":"department_3","RRRRR@Zurich.com":"department_3",
                     "SSSSS@Zurich.com":"department_4","TTTTT@Zurich.com":"department_4","UUUUU@Zurich.com":"department_4","VVVVVVV@Zurich.com":"department_4","WWWWWW@Zurich.com":"department_4","XXXXX@Zurich.com":"department_4"}
   
    User_department=User_department_dictionary['{}'.format(User_identification)]
    
    fisical_location_dictoanary={"department_1":"Spain","department_2":"France","department_3": "Italy","department_4":"Germany"}
    
    fisical_location=fisical_location_dictoanary['{}'.format(User_department)]
    
    Country_of_the_RU_the_department_work_with_dictionary={"department_1":"Spain","department_2":"Austria","department_3": "Estonia","department_4":"Greece"}
    
    Country_of_the_RU_the_department_work_with = Country_of_the_RU_the_department_work_with_dictionary['{}'.format(User_department)]
    
    #This columns will determine for every line in the dashboards which countryes that user have asked data from. 
    #To determine wheather the user wants data from a specific country or not I use probavility. 
    #if the department that makes the query works with a specific country, then the chances of this country eing queried is 97.5%, otherwhise its has just a provability of 2.5%. 
    #For example the department 1 works with "Spain" and thus, in 97.5% of the lines will ask for information from this country. 
    #These lines will put 1 if the user has asked for a specific country or 0 if it hasn't. 
    Spain = np.random.choice([1,0], p=[0.975 if Country_of_the_RU_the_department_work_with == "Spain"  else 0.025 , 0.025 if Country_of_the_RU_the_department_work_with == "Spain" else 0.975])
    Austria = np.random.choice([1,0], p=[0.975 if Country_of_the_RU_the_department_work_with == "Austria"  else 0.025 , 0.025 if Country_of_the_RU_the_department_work_with == "Austria" else 0.975])
    Belgium = np.random.choice([1,0], p=[0.975 if Country_of_the_RU_the_department_work_with == "Belgium"  else 0.025 , 0.025 if Country_of_the_RU_the_department_work_with == "Belgium" else 0.975])
    Croatia = np.random.choice([1,0], p=[0.975 if Country_of_the_RU_the_department_work_with == "Croatia"  else 0.025 , 0.025 if Country_of_the_RU_the_department_work_with == "Croatia" else 0.975])
    Denmark = np.random.choice([1,0], p=[0.975 if Country_of_the_RU_the_department_work_with == "Denmark"  else 0.025 , 0.025 if Country_of_the_RU_the_department_work_with == "Denmark" else 0.975])
    Estonia = np.random.choice([1,0], p=[0.975 if Country_of_the_RU_the_department_work_with == "Estonia"  else 0.025 , 0.025 if Country_of_the_RU_the_department_work_with == "Estonia" else 0.975])
    Finland = np.random.choice([1,0], p=[0.975 if Country_of_the_RU_the_department_work_with == "Finland"  else 0.025 , 0.025 if Country_of_the_RU_the_department_work_with == "Finland" else 0.975])
    France = np.random.choice([1,0], p=[0.975 if Country_of_the_RU_the_department_work_with == "France"  else 0.025 , 0.025 if Country_of_the_RU_the_department_work_with == "France" else 0.975])
    Germany = np.random.choice([1,0], p=[0.975 if Country_of_the_RU_the_department_work_with == "Germany"  else 0.025 , 0.025 if Country_of_the_RU_the_department_work_with == "Germany" else 0.975])
    Greece = np.random.choice([1,0], p=[0.975 if Country_of_the_RU_the_department_work_with == "Greece"  else 0.025 , 0.025 if Country_of_the_RU_the_department_work_with == "Greece" else 0.975])
    Hungary = np.random.choice([1,0], p=[0.975 if Country_of_the_RU_the_department_work_with == "Hungary"  else 0.025 , 0.025 if Country_of_the_RU_the_department_work_with == "Hungary" else 0.975])
    Ireland = np.random.choice([1,0], p=[0.975 if Country_of_the_RU_the_department_work_with == "Ireland"  else 0.025 , 0.025 if Country_of_the_RU_the_department_work_with == "Ireland" else 0.975])
    Italy = np.random.choice([1,0], p=[0.975 if Country_of_the_RU_the_department_work_with == "Italy"  else 0.025 , 0.025 if Country_of_the_RU_the_department_work_with == "Italy" else 0.975])
    Latvia = np.random.choice([1,0], p=[0.975 if Country_of_the_RU_the_department_work_with == "Latvia"  else 0.025 , 0.025 if Country_of_the_RU_the_department_work_with == "Latvia" else 0.975])
    Lithuania = np.random.choice([1,0], p=[0.975 if Country_of_the_RU_the_department_work_with == "Lithuania"  else 0.025 , 0.025 if Country_of_the_RU_the_department_work_with == "Lithuania" else 0.975])
    Luxembourg = np.random.choice([1,0], p=[0.975 if Country_of_the_RU_the_department_work_with == "Luxembourg"  else 0.025 , 0.025 if Country_of_the_RU_the_department_work_with == "Luxembourg" else 0.975])
    Malta = np.random.choice([1,0], p=[0.975 if Country_of_the_RU_the_department_work_with == "Malta"  else 0.025 , 0.025 if Country_of_the_RU_the_department_work_with == "Malta" else 0.975])
    Netherlands = np.random.choice([1,0], p=[0.975 if Country_of_the_RU_the_department_work_with == "Netherlands"  else 0.025 , 0.025 if Country_of_the_RU_the_department_work_with == "Netherlands" else 0.975])
    Poland = np.random.choice([1,0], p=[0.975 if Country_of_the_RU_the_department_work_with == "Poland"  else 0.025 , 0.025 if Country_of_the_RU_the_department_work_with == "Poland" else 0.975])
    Portugal = np.random.choice([1,0], p=[0.975 if Country_of_the_RU_the_department_work_with == "Portugal"  else 0.025 , 0.025 if Country_of_the_RU_the_department_work_with == "Portugal" else 0.975])
    Romania = np.random.choice([1,0], p=[0.975 if Country_of_the_RU_the_department_work_with == "Romania"  else 0.025 , 0.025 if Country_of_the_RU_the_department_work_with == "Romania" else 0.975])
    Slovakia = np.random.choice([1,0], p=[0.975 if Country_of_the_RU_the_department_work_with == "Slovakia"  else 0.025 , 0.025 if Country_of_the_RU_the_department_work_with == "Slovakia" else 0.975])
    Slovenia = np.random.choice([1,0], p=[0.975 if Country_of_the_RU_the_department_work_with == "Slovenia"  else 0.025 , 0.025 if Country_of_the_RU_the_department_work_with == "Slovenia" else 0.975])
    Sweden = np.random.choice([1,0], p=[0.975 if Country_of_the_RU_the_department_work_with == "Sweden"  else 0.025 , 0.025 if Country_of_the_RU_the_department_work_with == "Sweden" else 0.975])



#I put the fake data together in a dataframe
    customers.append([Query_date,date_name, User_identification,User_department,fisical_location, Country_of_the_RU_the_department_work_with, Spain, Austria,Belgium,Croatia,Denmark,Estonia,Finland,
                      France,Germany,Greece,Hungary,Ireland,Italy,Latvia,Lithuania,Luxembourg,Malta,Netherlands,Poland,Portugal,Romania,Slovakia,Slovenia,Sweden])

customers_df = pd.DataFrame(customers, columns=['Query_date', 'date_name', 'User_identification','User_department','fisical_location', 'Country_of_the_RU_the_department_work_with',
                                                "Spain", "Austria","Belgium","Croatia","Denmark","Estonia","Finland", "France","Germany","Greece","Hungary","Ireland","Italy","Latvia","Lithuania",
                                                "Luxembourg","Malta","Netherlands","Poland","Portugal","Romania","Slovakia","Slovenia","Sweden"]) 



#For every line of data I create a number that hast a mean 20 and a desviation of 4. 
#this number will be the number of days that exist between the day in which the query was lanched and the date that the user uses as "Starting date" for the query
List_of_numbers_for_start_date=[round(num, 0) for num in np.random.normal(20, 4, nr_of_customers)]


#For every line of data I create a number that hast a mean 4 and a desviation of 2. 
#this number will be the number of days that exist between the day in which the query was lanched and the date that the user uses as "End date" for the query

TEMP_List_of_numbers_for_finish_date=[round(num, 0) for num in np.random.normal(4, 2, nr_of_customers)]
#This "End number" will need to be 0 or more, because we cannot ask for Future data to the API since it just stores past data.
#In case the number choosen by the distribution are less than 0, then we transform them to 0.
List_of_numbers_for_finish_date=[]
for index, number in enumerate(TEMP_List_of_numbers_for_finish_date): 
   
    if number>=0:
        
        List_of_numbers_for_finish_date.append(number)
    else: 
        List_of_numbers_for_finish_date.append(0)


#We incorporate this numbers to the dataframes. 
customers_df["Number_of_days_from_current_date_minuts_start_query_date"]=List_of_numbers_for_start_date
customers_df["Number_of_days_from_current_date_minuts_finish_query_date"]=List_of_numbers_for_finish_date




#----------------------------------------------- Here I initiate the Transformation process ---------------------------------------------

#Then I filter out the queries that were done during the weekend.
Days_to_keep=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
customers_df=customers_df[customers_df.date_name.isin(Days_to_keep)]

#Also I create a index for the dataframe
customers_df['id'] = np.arange(1, len(customers_df) + 1)

#I then create a new column that will add, for every line the countries that a certain user has queried. 
#in this way I detect the lines that due to the random creation of the data have no queries asociated. 

customers_df["sum_of_queries"]=customers_df["Spain"]+ customers_df["Austria"]+customers_df["Belgium"]+customers_df["Croatia"]+customers_df["Denmark"]+customers_df["Estonia"]+customers_df["Finland"]+ customers_df["France"]+customers_df["Germany"]+customers_df["Greece"]+customers_df["Hungary"]+customers_df["Ireland"]+customers_df["Italy"]+customers_df["Latvia"]+customers_df["Lithuania"]+customers_df["Luxembourg"]+customers_df["Malta"]+customers_df["Netherlands"]+customers_df["Poland"]+customers_df["Portugal"]+customers_df["Romania"]+customers_df["Slovakia"]+customers_df["Slovenia"]+customers_df["Sweden"]
#Then I delete the lines that don't have any query. 
customers_df=customers_df[customers_df["sum_of_queries"]>0]                                                


#I drop the Na's that are cointained in the dataset. 
Data = customers_df.dropna()

#To siplify the machine learning process,  instead of  feeding the neural network and the Random forest the full date when the query was doen, I transorm the dates into "days" and months
#To do that, I start by making sure that the ciolumn "Query_date" is in date format. 
Data['Query_date'] = pd.to_datetime(Data['Query_date'])

#once this is done, I transform the dates in "day" and "month".
Data['day_of_date'] = Data['Query_date'].dt.day
Data['month_of_date'] = Data['Query_date'].dt.month.astype(str)


#Now, in order to avoid that our machin learning models get overfitted I will group the days in the month (1,2,3 ... 31) in 6 groups
#depending on the day of the month that the query was done.
#these groups will be: "First_5_days", "From_5_to_10", "From_10_a_15", "From_15_a_20", "From_20_a_25", "Last_days_of_month". 

Data.loc[Data['day_of_date'] <= 5, 'Num_day'] = 'First_5_days' 
Data.loc[(Data['day_of_date'] > 5) & (Data['day_of_date'] <= 10), 'Num_day'] = 'From_5_to_10' 
Data.loc[(Data['day_of_date'] > 10) & (Data['day_of_date'] <= 15), 'Num_day'] = 'From_10_a_15'  
Data.loc[(Data['day_of_date'] > 15) & (Data['day_of_date'] <= 20), 'Num_day'] = 'From_15_a_20'  
Data.loc[(Data['day_of_date'] > 20) & (Data['day_of_date'] <= 25), 'Num_day'] = 'From_20_a_25' 
Data.loc[Data['day_of_date'] > 25, 'Num_day'] = 'Last_days_of_month' 






#With the following two chunks of code, what I will do, is to calculate, for every department how many days have passed between their queries
#So if a department makes a query the first of May of 2020 and then an other query the sixth of May of 2020 I want to keep track of how many days there are between one and the other other queries 
#This will be usefull data for the neuroal network that will predict which departments will need to make a query a certain day. Because the logical thing to think is that the more time a departmet 
#has spend without making a query, the more proable it will be that they will need to do a new one.                       

def intervaled_cumsum(a, trigger_val=1, start_val = 0, invalid_specifier=-1):
    out = np.ones(a.size,dtype=int)    
    idx = np.flatnonzero(a==trigger_val)
    if len(idx)==0:
        return np.full(a.size,invalid_specifier)
    else:
        out[idx[0]] = -idx[0] + 1
        out[0] = start_val
        out[idx[1:]] = idx[:-1] - idx[1:] + 1
        np.cumsum(out, out=out)
        out[:idx[0]] = invalid_specifier
        return out



Data_result=pd.DataFrame()
for id_, department in enumerate(list_of_departments): 
        temporal=(Data[Data.User_department==department])
        Dates=pd.DataFrame()
        Dates["Query_date"]=pd.date_range(start="2019-01-01",end="2022-01-01")
        Dates=Dates.merge(temporal, on='Query_date', how='left')
        There_was_a_query=[]
        for i in Dates["id"]:
            if i >0: 
                There_was_a_query.append(1)
            else: 
                There_was_a_query.append(0)
        Dates["There_was_a_query"]    =   There_was_a_query                   
        Dates['Last_Occurence'] = intervaled_cumsum(Dates["There_was_a_query"])
        if department== "department_1": 
            Dates['Department_1_Days_since_last_query'] = Dates['Last_Occurence']
        
        if department== "department_2": 
            Dates['Department_2_Days_since_last_query'] = Dates['Last_Occurence']
            
        if department== "department_3": 
            Dates['Department_3_Days_since_last_query'] = Dates['Last_Occurence']
            
        if department== "department_4": 
            Dates['Department_4_Days_since_last_query'] =Dates['Last_Occurence']
            
            
       
        
        Data_result=pd.concat([Data_result,Dates])
        
#As we can see in the dataframe that we have untill this point the "Last_Occurence" column give us the information that we needed, but one day off
#this happends because it works by rows, and thus, when a new query is created the counter goes to 0.
#in other words, if the last query was does 7 days ago, and today we do a new query, the column "Last_Occurence" column will show 0 because we did a query today and thus 
#the numbers of days that have gone by from the last query is 0 (becayse we did it today) 
#However in the data line that stores informationa bout yesterday, we have the 7 days that has passet from the last query.

#So what we need to do now is to take this column one row down, so we have the "7 days" register in "today's" line. 

#To do that, we first transform the column into a list 
lista_last_occurence=Data_result['Last_Occurence'].tolist()

#We delete the last element of the list and at the same time add as a first element of the list a "nan".
lista_last_occurence=[np.nan]+lista_last_occurence[:-1]

#Now we create a new column named "Last_Occurence_Transported_one_day" that has all the data transported one day.
Data_result['Last_Occurence_Transported_one_day']=lista_last_occurence




#I apply the same to the columns for the individual departments

#depaprtment 1
lista_last_occurence_dep_1=Data_result['Department_1_Days_since_last_query'].tolist()
lista_last_occurence_dep_1=[np.nan]+lista_last_occurence_dep_1[:-1]
Data_result['Dep_1_Last_Occurence_Transported_one_day']=lista_last_occurence_dep_1

#depaprtment 2
lista_last_occurence_dep_2=Data_result['Department_2_Days_since_last_query'].tolist()
lista_last_occurence_dep_2=[np.nan]+lista_last_occurence_dep_2[:-1]
Data_result['Dep_2_Last_Occurence_Transported_one_day']=lista_last_occurence_dep_2

#depaprtment 3
lista_last_occurence_dep_3=Data_result['Department_3_Days_since_last_query'].tolist()
lista_last_occurence_dep_3=[np.nan]+lista_last_occurence_dep_3[:-1]
Data_result['Dep_3_Last_Occurence_Transported_one_day']=lista_last_occurence_dep_3

#depaprtment 4
lista_last_occurence_dep_4=Data_result['Department_4_Days_since_last_query'].tolist()
lista_last_occurence_dep_4=[np.nan]+lista_last_occurence_dep_4[:-1]
Data_result['Dep_4_Last_Occurence_Transported_one_day']=lista_last_occurence_dep_4

#Now that we have the "Last Occurence" by department we will create a new dataframe and we will get the information from the transported columns, 
#and we will group them by date.
#We do this because later we will group the information by dates (because we will need it grouped in this way for the neural network)
#and then get the data about how many days passed from the last query done by the different departments

columns_selected=["Query_date","Dep_1_Last_Occurence_Transported_one_day","Dep_2_Last_Occurence_Transported_one_day","Dep_3_Last_Occurence_Transported_one_day","Dep_4_Last_Occurence_Transported_one_day"]

Dates=pd.DataFrame()
Dates["Query_date"]=pd.date_range(start="2019-01-01",end="2022-01-01")#here we generate the dataframe with dates
How_long_since_last_query_by_department=Dates.merge(Data_result[columns_selected], on='Query_date', how='left') #here we merge the data 
How_long_since_last_query_by_department=How_long_since_last_query_by_department.fillna(0)#we fill the nans
How_long_since_last_query_by_department=How_long_since_last_query_by_department.groupby(by=["Query_date"], dropna=False).sum()#we group the data by date


Data_result = Data_result.dropna(subset=['User_department'])

#then we put the data that has been grouped back to the "Data_result" dataframe. 
Data_result=Data_result.merge(How_long_since_last_query_by_department, on='Query_date', how='left')   
        
       


Data_visualize=Data_result


#END OF THE CREATION OF THE FAKE DATA
#]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]


#--------------------------- Neuronal network to define which department will most likelly do a query ------------

import pandas as pd
import numpy as np
from sklearn import preprocessing
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix, precision_score, recall_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.utils.validation import column_or_1d


#I choose the columns that I will use for the variables X or Y

Columns_that_I_will_work_with=Data_result[["Query_date","date_name","day_of_date","month_of_date","User_department","Num_day","Dep_1_Last_Occurence_Transported_one_day_y","Dep_2_Last_Occurence_Transported_one_day_y","Dep_3_Last_Occurence_Transported_one_day_y","Dep_4_Last_Occurence_Transported_one_day_y"]]

#Here I'm grouping the data by date, so instead of having the different registers for every department that has 
#made a call that day, we have one register that contains all the departments that made a query that day.
Department_grouped_by_date_of_query=Columns_that_I_will_work_with.groupby('Query_date')['User_department'].apply(list)

Department_grouped_by_date_of_query_no_repetition=pd.Series.to_frame(Department_grouped_by_date_of_query.apply(lambda x: list(set(x))))

Columns_that_I_will_work_with=Columns_that_I_will_work_with.drop_duplicates(subset=['Query_date']).drop(columns="User_department")

Data_first_neural_network=Department_grouped_by_date_of_query_no_repetition.merge(Columns_that_I_will_work_with, on='Query_date', how='left')



#I transform the categorical data into dummies for the "X" variables
ohe_day_of_week = OneHotEncoder(sparse=False) 
dumies1=pd.DataFrame(ohe_day_of_week.fit_transform(Data_first_neural_network[['date_name']]))
#print(ohe_dia_semana.categories_) 
dumies1.columns=ohe_day_of_week.categories_


ohe_month = OneHotEncoder(sparse=False) 
dumies2=pd.DataFrame(ohe_month.fit_transform(Data_first_neural_network[['month_of_date']]))
#print(ohe_mes.categories_)
dumies2.columns=ohe_month.categories_


ohe_part_of_month = OneHotEncoder(sparse=False) 
dumies3=pd.DataFrame(ohe_part_of_month.fit_transform(Data_first_neural_network[['Num_day']]))
#print(ohe_parte_del_mes.categories_)
dumies3.columns=ohe_part_of_month.categories_




#I choose the only element that I will need from the dataset "Data_first_neural_network"
#since all the other needed columns have already been transformed to dummies
columns_I_want=["Dep_1_Last_Occurence_Transported_one_day_y","Dep_2_Last_Occurence_Transported_one_day_y","Dep_3_Last_Occurence_Transported_one_day_y","Dep_4_Last_Occurence_Transported_one_day_y"]
Last_Occurence_Transported_one_day_Column = Data_first_neural_network[columns_I_want]
#I continue by concatenating the different columns.
Data_first_neural_network_x=pd.concat([Last_Occurence_Transported_one_day_Column.reset_index(drop=True),dumies1,dumies2,dumies3],axis=1)


#To avoid problems,I transform the elements to float32 
Data_first_neural_network_x = np.asarray(Data_first_neural_network_x).astype(np.float32)

#I also apply some transformations to the columns that I am trying to predict (the departments)
#I start by getting the columns "User_Departments"
Data_first_neural_network_y = Data_first_neural_network["User_department"]

Y=np.array(pd.get_dummies(Data_first_neural_network_y.apply(pd.Series).stack()).sum(level=0))
#Then I apply the function column_or_1d and encode the column to avoid problems.




#now that already have the data in the format that I need, I divide the data into train and test
X_train ,X_test, Y_train, Y_test = train_test_split(Data_first_neural_network_x,Y,test_size=0.3)



#Now I create different layers of the neural network

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(units=128, activation='relu', input_shape=(27,)))
model.add(tf.keras.layers.Dense(units=300, activation='relu'))
model.add(tf.keras.layers.Dense(units=400, activation='relu'))
model.add(tf.keras.layers.Dropout(0.5))
model.add(tf.keras.layers.Dense(units=300, activation='relu'))
model.add(tf.keras.layers.Dense(units=400, activation='relu'))
model.add(tf.keras.layers.Dense(units=4, activation='sigmoid'))



model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

model.summary()

#I train the model with doing 100 epochs, which is uite hight, but it is not a problem since I have incorporated a dropout layer in the neural network
model.fit(X_train, Y_train, epochs=20, batch_size=10)



#I disactivate the following lines because they will show the results for the test data, but considering that 
#we are training the dataset with random data, this result doen't have much meaning
#test_loss, test_accuracy = model.evaluate(X_test, Y_test)
#print("Test accuracy: {}".format(test_accuracy))


#I print one prediction
print("\n"*4)
print("Predictions for the Departments for a certain day")   
print("\n")
Departments_likely_to_make_a_consult=[]
index_of_the_departments=[]
prediccio=model.predict(X_test)
for index,prediction in enumerate(prediccio[:1]):
    print("Array of predictions: ", prediction)
    Departments_likely_to_make_a_consult=[]
    for ind, element in enumerate(prediction): 
        if element > 0.70: 
            Departments_likely_to_make_a_consult.append(list_of_departments[ind])
            index_of_the_departments.append(ind)
    print(Y_test[index])

print("\n")

print("Position that have in the array of predicitons: ",index_of_the_departments)
print("Department/s Selected: ",Departments_likely_to_make_a_consult)

index_of_the_departments
print("\n"*4)            




#--------------------------- Start_date and Finish_date regressions






#I apply the same procedure that I have aplied before, but with the difference that now I'm includin the 
#User_department variable

#Now I'm trying to predict the number of days between the start day o the query.
ohe_day_of_week = OneHotEncoder(sparse=False) 
dumies1=pd.DataFrame(ohe_day_of_week.fit_transform(Data_result[['date_name']]))
#print(ohe_dia_semana.categories_) 
dumies1.columns=ohe_day_of_week.categories_


ohe_month = OneHotEncoder(sparse=False) 
dumies2=pd.DataFrame(ohe_month.fit_transform(Data_result[['month_of_date']]))
#print(ohe_mes.categories_)
dumies2.columns=ohe_month.categories_


ohe_part_of_month = OneHotEncoder(sparse=False) 
dumies3=pd.DataFrame(ohe_part_of_month.fit_transform(Data_result[['Num_day']]))
#print(ohe_parte_del_mes.categories_)
dumies3.columns=ohe_part_of_month.categories_



ohe_User_department = OneHotEncoder(sparse=False) 
dumies4=pd.DataFrame(ohe_User_department.fit_transform(Data_result[['User_department']]))
#print(ohe_parte_del_mes.categories_)
dumies4.columns=ohe_User_department.categories_

Data_to_predict_start_and_end_date_X=pd.concat([dumies1,dumies2,dumies3,dumies4],axis=1)




#------------------------------- Start Date -------------------------

Data_to_predict_starting_Y=Data_result['Number_of_days_from_current_date_minuts_start_query_date']



#I adapt the variable Y 
Data_to_predict_starting_Y2 = column_or_1d(Data_to_predict_starting_Y, warn=True)

from sklearn.preprocessing import LabelEncoder
lb=LabelEncoder()
Data_to_predict_starting_Y3=lb.fit_transform(Data_to_predict_starting_Y2)


#I separate the data in train and test
X_train ,X_test, Y_train, Y_test = train_test_split(Data_to_predict_start_and_end_date_X,Data_to_predict_starting_Y3,test_size=0.1)





from sklearn.tree import DecisionTreeRegressor

#In this case, I apply the Decission Tree regressor, since the data incorporates a lot of categorical data.
regressor = DecisionTreeRegressor()
regressor.fit(X_train,Y_train)


#I akks the model to do a prediction 
y_pred_date_start=regressor.predict(X_test)


#and I print the first 10 predictions and the first 10 numbers of the Y_test" to check how accurate the predictions are. 
print("Predictions for the Start Date") 
print("\n")
for index, element in enumerate(y_pred_date_start[:10]):
    
    print("prediction: ", round(element), "real number: ", Y_test[index])







#---------------------- Date End -----------------------



#I follow the same procedure with the "End" date now.
Data_to_predict_End_Y=Data_result['Number_of_days_from_current_date_minuts_finish_query_date']


Data_to_predict_end_Y2 = column_or_1d(Data_to_predict_End_Y, warn=True)


lb=LabelEncoder()
Data_to_predict_end_Y3=lb.fit_transform(Data_to_predict_end_Y2)

X_train ,X_test, Y_train, Y_test = train_test_split(Data_to_predict_start_and_end_date_X,Data_to_predict_end_Y3,test_size=0.3)


regressor = DecisionTreeRegressor()
regressor.fit(X_train,Y_train)

y_pred_date_end=regressor.predict(X_test)

print("\n"*2)
print("Predictions for the End Date")   
print("\n")
for index, element in enumerate(y_pred_date_end[:10]):
    
    print("prediction: ", round(element), "real number: ", Y_test[index])







from datetime import date
import datetime

print("\n"*5)


#The following code is just an example. it is just to comprehend how, by having the different elements that 
#we have predicted, we can make a query to the source API. 

today = date.today()

print("The departments selected are: ", Departments_likely_to_make_a_consult)
print("\n"*3)

#Query that would be launched to the sourcre API 
for index, element in enumerate(Departments_likely_to_make_a_consult): 
    print("The program would ask to the API for data of {} from {} until {}".format(fisical_location_dictoanary[element], today- datetime.timedelta(int(y_pred_date_start[index])), today- datetime.timedelta(int(y_pred_date_end[index]))))
    print("")
    print("Since: ")
    print("The ", element, "works for ", fisical_location_dictoanary[element])
    print("")
    print("And:")
    print("The current data is: ", today)
    print("")
    print("Thus, if the example of number of days for the starting date:", round(y_pred_date_start[index]), " and the example of end date is ", round(y_pred_date_end[index]), " then the start date is ", today- datetime.timedelta(int(y_pred_date_start[index])), "and then end date is ", today- datetime.timedelta(int(y_pred_date_end[index])))
    print("\n"*2)
    print("------------------")      
          
    print("\n"*2)
    

#The error for both, the neural network and the regressions, can be explained for two reasons: 
    #there is not enought data
    #the data is generated randomly and thus most of the correlation that would exit in real data does not exist. 

