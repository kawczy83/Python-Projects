import pandas as pd
import matplotlib.pyplot as plt

#import data from: https://www.kaggle.com/rush4ratio/video-game-sales-with-ratings
games = pd.read_csv("Video_Games_Sales.csv")

#drop na values
games = games.dropna(axis=0)

#change types
games['User_Score'] = pd.to_numeric(games["User_Score"]) 
games['User_Score'] = games["User_Score"] * 10
games['Year_of_Release'] = games.Year_of_Release.astype(str)

#subset data into different categories
mario = games[games['Name'].str.contains("Mario")]
mario['Category'] = "Mario"

gta = games[games['Name'].str.contains("Grand Theft Auto")]
gta['Category'] = "GTA"

cod = games[games['Name'].str.contains("Call of Duty")]
cod['Category'] = "CoD"

#combine datasets
mario_cod = pd.merge(mario,cod,how='outer') #combine Mario and Call of Duty datasets together
combined = pd.merge(mario_cod, gta, how='outer') #combine everything together

#Data Visualization Charts:
#mario
plt.scatter(mario['Critic_Score'],mario['User_Score'])
plt.xlabel("Critic Score")
plt.ylabel("User Score")

#grand theft auto
plt.scatter(gta['Critic_Score'],gta['User_Score'])
plt.xlabel("Critic Score")
plt.ylabel("User Score")

#call of duty
plt.scatter(cod['Critic_Score'],cod['User_Score'])
plt.xlabel("Critic Score")
plt.ylabel("User Score")

#all together
plt.scatter(combined['Critic_Score'],combined['User_Score'])
plt.xlabel("Critic Score")
plt.ylabel("User Score")

#Visualizes yearly sales from 1998 to 2016 of three of the most popular video game franchises globally
yearlySales = combined.groupby(['Year_of_Release','Category']).Global_Sales.sum()
yearlySales.unstack().plot(kind='bar',stacked=True, colormap= 'Reds', 
ylim=(0,80), grid=False)
