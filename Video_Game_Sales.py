import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#import data from: 
#https://www.kaggle.com/rush4ratio/video-game-sales-with-ratings
games = pd.read_csv("Video_Games_Sales.csv")

#drop na values and show games 
#that sold more than a million copies globally
games = games.dropna()
games = games[games['Global_Sales'] > 1]

#change types
games['User_Score'] = pd.to_numeric(games["User_Score"],errors='coerce') 
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
mario_cod = pd.merge(mario,cod,how='outer')
combined = pd.merge(mario_cod, gta, how='outer')

#add new column: differences between Critics and Users
combined['Diff'] = combined['Critic_Score'] - combined['User_Score']
#charts
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

#all together - with matplotlib
plt.scatter(combined['Critic_Score'],combined['User_Score'],
            label='Category')
plt.xlabel("Critic Score")
plt.ylabel("User Score")
#all together - with seaborn
sns.set(style="white")
g = sns.lmplot(x = 'Critic_Score',
           y = 'User_Score',
           data=combined, 
           fit_reg=False, 
           hue="Category",
           palette="Set1")
sns.despine(top=True, right=True, left=True, bottom=True)
g = (g.set_axis_labels("Critic Score", "User Score")
.set(xlim=(0, 100), ylim=(0, 100)))

yearlySales = combined.groupby(['Year_of_Release','Category']).Global_Sales.sum()
yearlySales.unstack().plot(kind='bar',stacked=True, colormap= 'Reds', 
ylim=(0,80), grid=False)
