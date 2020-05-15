
#In this file I will analyze the data from a business that once a year creates a 
#marketing campaign to try to seel 5 different offers to its clients.
#The business wants to know how to maximize the number of offers that are accepted by
#its clients. Because of that, I will analyze how the different features of the dataframe 
#increase or decrease the possibilities that the customers accept those offers.


data=read.csv("marketing_campaign.csv",sep=";")


#---------------------------------- Cleaning the data ----------------------------------

length(data[is.na(data)])
#There are 24 NA's since this dataset has a lot of registers, 24 of them won't make any important difference, I will delete the rows
data=data[complete.cases(data), ]


#I'm deleting the column ID since it is an irrelevant information.
data=data[,-1]

#Now that I have already deleted the misleading rows and there are no more NA's or other strange symbols, 
#I can proceed to analyze the data.


#---------------------------------- analyzing the data -------------------------------

library(ggplot2)

#The business wants to know how to increase the possibilities that a customer accepts an offer. 
#According to what I can see in the dataframe, there has been 5 marketing campaigns, because there 
#are 5 features that make reference to who has accepted and who refused the offer
  #(data$AcceptedCmp1, data$AcceptedCmp2, data$AcceptedCmp3, data$AcceptedCmp4, data$AcceptedCmp5)

#what I will do is to create a new feature to see how many offers has accepted every client and if there is a relation 
#As I said, in the dataset there are 5 features that indicate whether the customer accepted the first offer (0 if no 1 if yes), the second, the third
#the fourth and the fifth. It is possible to add these 5 variables to see how many offers has a client accepted, since every accepted 
#offer figures as 1 and every non-accepted offer is equal to 0, if a certain customer has a 4 in the new column, that would mean 
#that he/she accepted 4 out of the 5 offers.

num.accepted=data.frame("num accepted"=data$AcceptedCmp1+data$AcceptedCmp2+data$AcceptedCmp3+data$AcceptedCmp4+data$AcceptedCmp5)


#The order I will follow to analyze the variables will be, selecting the feature that I thing, will be 
#the most important one and then I will continue my analysis linking the other features.



table(data$Year_Birth)

#The first thing I can notice about this dataset is that a lot of the registers 
#are from people born between 1970 and 1980. I will create a table with the 
#frequencies of the year of birth of the different participants

sort(table(data$Year_Birth),decreasing=T)[1:5] 

#Now, I will complete the information with a histogram to see the distribution of the ages 
#I assume that this business has that many data from people born in the 70's because this is their 
#main customer target. However, I should also highlight the important number of people born in the 
#50's and 60's.

cuts=data.frame(cuts=(cut(data$Year_Birth,breaks = c(1850,1940,1950,1960,1970,1980,1990,2000),labels = c("30's or older","40's","50's","60's","70's","80's","90's"))))

library(dplyr)
table(cuts) %>% 
  as.data.frame() %>% 
  ggplot(aes(x = cuts, y = Freq, fill=cuts)) + 
  geom_col()+
  labs(x="Groups of age", y="Frequency",  title="Ages of the customers"    )+
  theme(legend.position = "none") 

#I will continue including the number of offers accepted to the dataframe "cuts" and watching how many offers 
#did the customers from different age groups accepted.

cuts=cbind(cuts,num.accepted)
prop.table(table(cuts$cuts,cuts$num.accepted),1)


#The resulting table shows which percentage of customers of every decade accepted 0,1,2,3 or 4 offers
#for example, the 68.65% of people from the 40's did not accept any offer, 20.89 % accepted 1,
#8.95% accepted 2 and 1.49 % accepted 3. 

#If, as I said, the main target of the business is the people from the 70's, then, I would recommend to change it, because
#this is the decade that shows a smaller percentage of acceptance. 83.78% of them didn't accept a single offer 
#and less than 5% accepted 2 or more offers (2.43%+2.29%+0.14%)
#The groups that show the best percentages for the business are the customers born in the 90's and the ones born in the 40's.



cuts$Income=data$Income
aggregate(Income~cuts, data = cuts, FUN = mean)

#If we make a comparison of the mean incomes by groups, it is possible to see that the wealthiest groups are the 40's and the 90's, 
#and thus, this are again the ones with the best potential.

#Considering that the mean income for the persons who were born during the 70's is the second lowest, maybe, the high percentage 
#of rejection of the offers is due to a reduced income. In order to learn more about that, I will examine if the income has an important
#effect on whether the person accepts the offers or not. I assume that the costumers with less money will be more conservative when it comes 
#to decide whether to accept or decline an offer that is not expected.

#I will create a table with the number of offers that the customers have accepted and whether their income is more than 50000$ or not. 
#In the following table, FALSE will mean that they earn less than 50000$ and TRUE will mean that they earn more than that.

prop.table(table(cuts$Income>50000,cuts$num.accepted),1)

#As we can see, 90% of those who earn less than 50000 have rejected all the offers and if they have accepted any, they mostly accepted just one. 
#The costumers who earn more than 50000$ show a different behavior. More than 30% of the clients who have 
#an income greater than 50000$ have accepted at least one offer, almost 1% of these customers accepted up to 4 offers.



#Since the income is such an important factor, and it is related to the level of studies, maybe the education will be 
#Another important factor. I will create a boxplot to see the distribution of the incomes based on the education
#I think it will show that the people with lower education earn less and if this is the case, I will assume that most of the 
#customers with less studies show less inclination to accept the offer.

data$Education=factor(data$Education, levels=c("Basic","2n Cycle","Graduation","Master","PhD"))

ggplot()+
  geom_boxplot(aes(data$Education,data$Income))+
  coord_cartesian(ylim = c(0, 200000))+
  labs(x="Level of education", y="Income", title="Level of education vs Income")

#As I said, the people with Basic education earns less than the clients with more studies.
#I will now proceed to see if it is also true that most of the people with basic education refused the offer.

prop.table(table(data$Education,cuts$num.accepted),1)

#As we can see, the clients that studied the most are more likely to accept the offer of the supermarket. 
#We can conclude then that the level of studies and the income share great similarities and that they are a 
#great factor to determine how the client will act. 



#Another factor that can also influence the decision of the costumer is whether they have Kids or not and if they have Teenagers at home. 
#I will start by introducing the information in the dataset "cuts", and making a bar plot.

cuts$Kid=as.factor(data$Kidhome)

ggplot()+
  geom_bar(aes(cuts$num.accepted,fill=cuts$Kid),position="fill")+
  labs(x="number of offers accepted", y="Count", title="From the Total, % that represents every group")+
  scale_fill_discrete(name = "Number of kids")
prop.table(table(cuts$Kid,cuts$num.accepted),2)

#The plot that I have made has the position="fill". That means that it shows the percentage of clients that did a certain thing.
#For example, as we can see, the whole bar of 4 offers accepted, is filled with the color of "0 kids". 
#That means that 100% of the clients who took 4 offers had 0 kids. 
#The table that I made after the plot, explains the same information but showing the exact numbers.



#If I apply the same procedure with the number of teenagers that the customer has we see a similar trend, but in a more moderated way.

cuts$teen=as.factor(data$Teenhome)

ggplot()+
  geom_bar(aes(cuts$num.accepted,fill=cuts$teen),position="fill")+
  labs(x="number of offers accepted", y="Count", title="From the Total, % that represents every group")+
  scale_fill_discrete(name = "Number of teenagers")

prop.table(table(cuts$teen,cuts$num.accepted),2)
0.098765432 +0.090909091

#We can conclude the analysis of kids and teenagers saying that this a very influential factor, especially if the consumers has kids. 



#Now I will take a closer look at the kind of food that the clients buy and if these habits make a difference when it comes to take decisions regarding the offers
#I will start creating a new dataframe named "food" with the data that makes reference to food and drinks.
#I will also include the number of offers that the clients have accepted, and I will use a boxplot to examine it better.

food=data.frame("Wine"=data$MntWines,"Fish"=data$MntFishProducts,"Fruits"=data$MntFruits,"Meat"=data$MntMeatProducts,"Sweet"=data$MntSweetProducts,"Gold"=data$MntGoldProds)
food$offer=factor(cuts$num.accepted)

library(reshape)

meltData <- melt(food)
ggplot(meltData)+
  geom_boxplot(aes(factor(variable), value, color=offer))+ 
  labs(x="Line of products", y="consumer spending", title="Dolars spent per line of products based on the offers accepted")+
  scale_fill_discrete(name = "Offers accepted")

#This is a very interesting plot, there are a couple of important ideas we can obtain from it: 
  #1-Generally, the persons who buy more tend to be more open to the offers. Even if it is more difficult to 
    #detect a client willing to accept 4 offers, to focus on the clients whose consume is higher than the 95th percentile, 
    #of its respective line of products, increases greatly the possibilities to contact consumers who will accept 2 or 3 offers.
  #2-The consumption of wine is a very good indication of how interested a certain customer could be. 



#The following function will determine the different quartiles; the business should target any person who
#buys products from ANY line with a total cost that overpasses the top 5 %

meltData=data.frame(meltData)
library(dplyr)

summary(A)
summary(food)
meltData%>%
  group_by(variable)%>%
  summarise("10%"=quantile(value, 0.95, na.rm=TRUE))

# Wine     1000
# Fish      169 
# Fruits    122
# Meat      688
# Sweet     125
# Gold      165

meltData=data.frame(meltData)

A=meltData[(meltData$variable=="Wine" & meltData$value>1000)|(meltData$variable=="Fish" & meltData$value>169)|(meltData$variable=="Fruits" & meltData$value>122)|(meltData$variable=="Meat" & meltData$value>688)|(meltData$variable=="Sweet" & meltData$value>125)|(meltData$variable=="Gold" & meltData$value>165),]

table(A$offer!=0) 

#As we can see in the last table, if the business targets just the people in upper 5% of consumption
#the possibilities of reaching a client that accepts at least one offer is almost the same as the possibility of him/her rejecting it. 
317/(348+317)


#Regarding the wine consumption distinction of the clients that I said in the second point, 
#as we can see in the plot.

ggplot(meltData)+
  geom_boxplot(aes(factor(variable), value, color=offer))+ 
  labs(x="Line of products", y="consumer spending", title="Dolars spent per line of products based on the offers accepted")+
  scale_fill_discrete(name = "Offers accepted")

#If from the wine line of products, we take the consumers that have a consumed a wine with a total cost that 
#overpasses the median cost of the group of consumers that accepted 2 offers, the possibilities to find a 
#client that who REFUSES the offer decreases greatly

food%>%
  select(Wine,offer)%>%
  group_by(offer)%>%
  summarise("summary"=median(Wine))

table(food[food$Wine>822,"offer"]!=0)

#As we can see from all the consumers who have payed more than 822$ for wine during 2 years, 
#70 would say no to the offer and 153 would accept at least one offer, that gives us a ratio of success of
153/(153+70) #68.60%



#We now know what the customers buy, now is time to understand how the buy, because according to many studies this is one of the most 
#important aspects to consider when choosing how to address the consumer.

Buy=data.frame("Deals"=data$NumDealsPurchases,"Web"=data$NumWebPurchases,"Catalog"=data$NumCatalogPurchases,"Store"=data$NumStorePurchases,"Visit_web"=data$NumWebVisitsMonth)
Buy$offer=factor(cuts$num.accepted)

meltData <- melt(Buy)

ggplot(meltData)+
  geom_boxplot(aes(factor(variable), value,color=offer))+
  labs(x="How costumers buy", y="Count")+
  scale_fill_discrete(name = "Offers accepted")

#From this last plot it is possible to obtain 3 interesting information: 
  #1-Eventhoug the behavior that the clients have depend on how they buy (trough web, using catalog or in the physical shop)
  #if what we want to know is how do we maximize the possibilities to contact a costumer who at least accepts one offer, 
  #then the output that we get from this plot is the same as the last one, the more the client buys, the more likely hi/she 
  #is to accept it, no matter how they buy. 

  #2- Another important conclusion that we can take out of this chart is that according to the data, 
  # the consumers who constantly visit the webpage tend to refuse the offers
  prop.table(table(Buy$offer,Buy$Visit_web),2)
  #according to the data, the customers who visited the webpage more than 9 times in 1 month 
  #will reject the offer in almost every case.
  
  #3- The last interesting conclusion we can obtain from this plot is that the more deals a customer buys 
  #the less tendency he/she will have to accept an offer. The data reveals that the customers who are more
  #likely to accept the offer have bought 0 or 1 discounted products in the last month
  
  Buy%>%
    select(offer,Deals)%>%
    group_by(offer)%>%
    summarise("Less than"=quantile(Deals, 0.5, na.rm=TRUE))
  
  Discout=Buy[Buy$Deals>1,"offer"]
  table(Discout!=0)
  
#As we can see in the table only 15.67% (190/(1022+190)) of those who bought more than one discounted item 
#accepted any offer. That's why I would recommend to focus on those who bought 1 or less discounted items.
  
  
  
#One of the most important points to talk about when it comes to whether a consumer will buy in a certain store 
#is how happy this consumer is, and the feature "complain" will help us to understand that. 
#this variable explains if the costumer complained to the costumer in the last 2 years.
  
prop.table(table(data$Complain,cuts$num.accepted),1)

#With a table, we can see that the clients who complained show 
#a lower percentage of acceptance, 90% of then refused all the offers.



#I will finish this analysis by extracting some ideas from the variables that refer to time: 
  #Dt_Customer : date of customer's enrolment with the company
  #Recency : number of days since the last purchase



#I will examine first the Dt_Customer, this may seem an irrelevant data, 
#however, it has been proven by many studies that the day of the week in which people buy show a certain pattern of behavior. 
#For example, the person who goes to the supermarket on Saturday tend to buy larger quantities of food than those who go during the week,
#since these last ones, tend to go at least 2 time per week to buy groceries.

#Before applying the next function, I should clarify that, it
#transforms a date into de day of the week. It is a Spanish function and thus the days 
#of the week will be in Spanish, here you have the translation:


  #lu// -> lunes ->     Monday
  #ma// -> martes ->    Tuesday
  #mi// -> miercoles -> Wednesday
  #ju// -> jueves ->    Thursday 
  #vi// -> viernes ->   Friday
  #sa// -> sabado ->    Saturday
  #do// -> domingo ->   Sunday


library(lubridate)

time=data.frame("Recency"=data$Recency,"Date_customer"=data$Dt_Customer)

daily=time%>%
  mutate(wday=wday(Date_customer,label=TRUE))#la funciò wday es una funciò per transformar una data de format YYYY-MM-DD en el nom (dilluns, dimars, dimecres...)

day=factor(daily$wday,levels=c("lu\\.","ma\\.","mi\\.","ju\\.","vi\\.","sá\\.","do\\."))

prop.table(table(day,cuts$num.accepted),1)

#Even though the most of the percentual differences that exist between days are irrelevant, 
#there is 1 fact that worth mentioning. 
#The customers who enrolled to the company on Thursday or Friday are less likely to accept the offer. 
#It may seem a non-relevant data, however after seeing that the difference between the costumers who 
#enrolled on Monday and those who enrolled on Thursday is more than 7%, I think is something that needs to be considered. 



#Regarding the Recency feature, I will start by plotting the data.

table(time$Recency)

ggplot()+
  geom_bar(aes(time$Recency,fill=factor(cuts$num.accepted)))+
labs(x="Days since the last purchase", y="count", title="Days since the last purchase vs offers accepted")+
  scale_fill_discrete(name = "Offers accepted")

#There is no sign of a pattern in the plot nor in the table. I will try to cut the data in different groups 
#grouping the days in weeks. For example, the first group will group all the customers who 
#went to by less than 7 days ago, the next group will have the customers who went between 7 and 14 days ago...

days=cut(time$Recency,c(-0.1,7,14,21,28,35,42,49,56,63,70,77,84,91,98,105),levels=c("7","14","21","28","35","42","49","56","63","70","77","84","91","98","105"))
prop.table(table(days,cuts$num.accepted),1 )

#In my opinion, more data would be required in order to get a good conclusion out of this data. 
#However, the numbers reveal a certain patter that is very interesting. The percentage of customers 
#who refused all the offers, reach the lower points during the following periods:

  #From 7 days to 14: 77% didn't accept any offer
  #From 21 days to 28: 73% didn't accept any offer
  #From 28 days to 35: 74% didn't accept any offer
  #From 56 days to 63: 75% didn't accept any offer

#The rest of percentages are closer or above 80%.

#This data is interesting because it is possible to see that: 
  #1-The customers follow a certain pattern. They are more likely  to accept at least one offer after a week (from 7 days to 14), after a month (21 days to 35), after two months (from 56 days to 63)
  #2-Most of the "optimal time" to make the offer to the costumer are during the first month. 

#These two conclusions could be explained because according to psychology principles: people is more likely to spend their money in a business that they have already bought in, because they 
#feel linked to it, this link disappears with time.



#---------------------------------- Conclusions of the analysis -------------------------------



#In this conclusion I will explain the most interesting data that we can extract from the data. 
#I will divide it in three different parts, family and finances, habits, and time. The first part will be more focused on which group of consumers should be targeted for the offers that the business makes. In the second one I will be explaining how to increase the success of the marketing campaigns. The last one will be more anecdotical, some data to consider but not to as important as the data explained in the habits part.

#Family and finances: 
#The customer target of the business, according to the amount of data that the business has, seems to be people born in the decade of the 70's. However, this is the customer that tends to reject the most offers. According to the data, 83.78% of the consumers born in the 70's refused all the marketing campaigns that the business made, and just 5% accepted 2 or more of them. In contrast, just the 67.44% of those born in the decade of the 90's rejected all the offers and 13.95% of them accepted 2 of more offers.
#Another important factor to decide who should the business marketing campaigns focus to, is the personal finances. Even though people born in the decade of the 70's may seem to have one of the biggest budgets to spend, the data reveals that in fact they are the second demographic group with less income, the first one is the group born in the decade of the 80's. 
#To determine if the Income was a decisive factor to decide of the customer would accept or decline the offer I created a table of percentages where it is possible to see that those consumers who earn less than 50000 $ per year, show a 90% provability of refusing the offer and those who earn more than that have a provability of just 69%.
#As we have seen with the data, the best groups, both in percentage of offer acceptance and the highest budget are the customers born in the decade of the 40's and the 90's. 

#Another very important point to consider is if the consumer has kids of teenagers. 
#The data shows that the customers who have kids or teenagers tends to prefer to refuse all or most of the offers, in fact, the consumers who have kids represent just the 18.96% of all the consumers who accepted 2 or more offers. It is worth saying that the situation is more moderated when the costumers have teenagers instead of kids. 

#Habits: 
#In this habits part, I will explain 2 very interesting facts that seem to be crucial when explaining why some costumers refuse the offers and others accept them, which products do they consume and how they buy their groceries. 
#From plot that explains which lines of products do the consumers buy, there are 2 important facts to highlight. 
#The fist one is that in all the of the product lines, but the wine one, a pattern has appeared. The level of spending shows a positive correlation with the number of offers accepted from 1 offer until 3 and then the level of consume reduces, the consumers who accepted 4 offers, show a low spending. 
#If the business just contacts the consumers who's spending is in the top 5% of the different lines of products, the possibility of finding a client who will accept at least 1 offer is 47.6%
  
#The second important fact that it is possible to see in the plot is that the consume of wine is one of the best indicators. The more a consumer spends in wine, the more possible is for him to accept an offer. If the business contacts those consumers who have a level of spending higher 822 the possibilities to fins a client who will accept at least 1 offer if 68.60%
#Obviously two facts have a certain relation with the income of the consumers that I highlighted in the "Family and finances" part. However, to know the influence that the level of spending has, is very important for the business since it will always be able to know who are the clients who consume the most.

#Another important fact is that according to the data, the consumers who visit the business webpage are less likely to accept the offers. From those consumers who visited the web more than 9 times during the last month, just one accepted one offer.
#A similar pattern appears with the number of discounted products that the consumer has bought during the last month. The customers who bought more than 1 discounted product in the last month have a probability of just 15.67% to accept one offer or more. 
#The last conclusion the business should consider regarding the habits of the consumer is that if a client has complained about the business in the last 2 years, they have a probability of 90% to reject all the offers.

#Time: 
#Before finishing the conclusion, I would like to highlight two facts that, in my opinion, are important to consider. 
#According to the data the costumers who enrolled to the company on Thursday or Friday are less likely to accept the offer. In fact, those who enroller on Monday have a probability to accept 7% higher than the costumers enrolled on Thursday.

#The data also reveals that the customers are more likely to accept an offer if they are contacted during the following periods after the last time they shop from the business:
  #-From 7 days until 14
  #-From 21 days to 28
  #-From 28 days to 35
  #-From 56 days to 63












