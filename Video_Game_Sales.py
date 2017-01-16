# The main purpose of this project is to determine if a video game's overall overratedness (where the game has a higher opinion 
# than is deserved) would have any correlation to game sales.  This project will also reveal which video game genres, publisher's (who published
# the game), and platform's (another name for console) are the most overrated.

import pandas as pd

# import data from: 
# https://www.kaggle.com/rush4ratio/video-game-sales-with-ratings
games = pd.read_csv("Video_Games_Sales.csv")

# drop rows that contain NA values
games = games.dropna()
# keeps Games that have sold at least 1 million copies worldwide
games = games[games['Global_Sales'] > 1]

# change types
games['User_Score'] = pd.to_numeric(games["User_Score"]) 
games['User_Score'] = games["User_Score"] * 10
games['Year_of_Release'] = games.Year_of_Release.astype(str)

# add new column, Diff: difference between Critics and Users, which measures 
# if a game is overrated (diff score is positive/critics score is higher than
# user score) or underrated (diff score is negative/user score is higher than
# critic score)
games['Diff'] = games['Critic_Score'] - games['User_Score']

# Displays the value counts of each Column 
[games['Publisher'].value_counts(),
games['Genre'].value_counts(),
games['Platform'].value_counts(),
games['Developer'].value_counts(),
games['Rating'].value_counts()]

# drop rows that contain the 'Platform' value, "PC" from the dataset, as I found
# that the numbers for PC games are underreported.
games_no_pc = games[games['Platform'] != "PC"]

# Creates dataset that shows Publishers that have more than 5 games that have
# sold more than a million copies globally. 
games_no_pc2 = games_no_pc.groupby("Publisher").filter(lambda x:len(x) >= 5)

games_no_pc2['Critic_Score'].mean()
games_no_pc2['Critic_Score'].std()

games_no_pc2['User_Score'].mean()
games_no_pc2['User_Score'].std()

# Reveals mean Diff scores by Genre,Platform, and Publisher and sorts them in 
# descending order.
genre1 = games_no_pc2.groupby(['Genre'])['Diff'].mean()
genre1.sort_values(ascending=False)

genre2 = games_no_pc2.groupby(['Genre'])['Global_Sales'].mean()
genre2.sort_values(ascending=False)

# I've found that the most overrated genre is Sports with a mean score of 8.17
# and the most underrated genre is Strategy with a mean score of -3.83.

platform1 = games_no_pc2.groupby(['Platform'])['Diff'].mean()
platform1.sort_values(ascending=False)
# I've found that the most overrated platform is the Xbox One with a mean score 
# of 17.74 and the most underrated platform is the GameCube with a mean score 
# of -3.75.

publisher1 = games_no_pc2.groupby(['Publisher'])['Diff'].mean()
publisher1.sort_values(ascending=False)

publisher2 = games_no_pc2.groupby(['Publisher'])['Global_Sales'].mean()
publisher2.sort_values(ascending=False)

# I've found that the most overrated publisher is Bethesda Softworks with a 
# mean score # of 10.5 and the most underrated publisher is 505 Games with 
# a mean score of -10.6.

# Finds  correlations within the Diff column.
games_no_pc2.corr()['Diff']

# The column with the biggest correlation with Diff is User_Score with a score
# of -0.6 (rounded two decimal places).  Which means as User_Score increases,
# Diff scores decreases.

#combines genre1 and genre2 together as a (12,2) matrix
# Strong correlation (0.505587) between Global Sales and Diff by Genre
pd.concat([genre1,genre2],axis=1) 
pd.concat([genre1,genre2],axis=1).corr()

# Weak correlation (0.134736) between Global Sales and Diff by Publisher
pd.concat([publisher1,publisher2],axis=1)
pd.concat([publisher1,publisher2],axis=1).corr()
