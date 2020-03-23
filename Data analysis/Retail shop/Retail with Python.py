import pandas as pd 
import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt

data = pd.read_excel("Retail.xls")
print(data.head())
print(data.dtypes)
print(type(data))

profit=pd.DataFrame(data.groupby("Country").sum()["Profit"])
print(profit)
Country=profit.index.tolist()
print(Country)
profit["Country"]=Country


profit=profit.sort_values("Profit",ascending=False)
print(profit)

profit2=pd.concat([profit.head(),profit.tail()])

print(profit2.columns)

sns.barplot(profit2["Profit"],profit2["Country"])
plt.show()

#-----------------------------------------------------------------

sales=pd.DataFrame(data.groupby("Country").sum()["Sales"])
print(sales)
Country=sales.index.tolist()
sales["Country"]=Country
sales=sales.sort_values("Sales",ascending=False)
print(sales)
sales2=sales.head(6)

sns.barplot(sales2.Sales,sales2.Country)
plt.show()
#---------------------------------------------------------------

sns.scatterplot(data.Sales,data['Shipping Cost'],hue=data.Category)
plt.show()
#--------------------------------------------------------------

sns.scatterplot(data.Category,data.Profit,hue=data["Sub-Category"],legend=False)
plt.show()
data2=data[data.Profit<-2000]

sns.scatterplot(data2.Category,data2.Profit,hue=data2["Sub-Category"],legend=False)
plt.show()
#------------------------------------------------------------------------

data_sub=pd.DataFrame(data.groupby("Sub-Category").sum()["Profit"])
Sub=data_sub.index.tolist()
data_sub["Sub-Category"]=Sub
data_sub=data_sub.sort_values("Profit",ascending=False)

sns.barplot(data_sub.Profit,data_sub["Sub-Category"])
plt.show()
#------------------------------------------------------------------------

data[(data["Sub-Category"]=="Machines") & (data.Profit<-2000)]["Product Name"]




data[data["Product Name"].str.contains("Cubify CubeX 3D")][["Product Name","Profit"]]

data[data["Product Name"].str.contains("Cubify CubeX 3D")]
  

#------------------------------------------------------------------------



data_USA=data[data.Market=="US"]

sns.boxplot(data_USA.Region,data_USA.Profit,showfliers=False)
plt.show()

#-----------------------------------------------------------------------

sns.countplot(data_USA["Order Priority"],hue=data_USA.Region)

#-----------------------------------------------------------------------


cross=pd.crosstab(data_USA["Order Priority"], data_USA['Category'], rownames = ['Order Priority'], colnames = ['Category'],margins=True)
print(cross/cross.iloc[-1,-1])


#-----------------------------------------------------------------------
sns.countplot(data_USA["Category"],hue=data_USA["Order Priority"])


#-----------------------------------------------------------------------


USA_consumer=data_USA[data_USA.Segment=="Consumer"]

#----------------------------------------------

axes = pd.tools.plotting.scatter_matrix(USA_consumer.iloc[:,18:23])
plt.tight_layout()

print(USA_consumer.iloc[:,18:23].corr())


#---------------------------------------------

sns.scatterplot(USA_consumer['Shipping Cost'],USA_consumer.Sales,hue=USA_consumer['Order Priority'])
plt.show()