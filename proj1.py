import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

matches = pd.read_csv(r"C:\Users\LENOVO\Downloads\matches.csv")
deliveries = pd.read_csv(r"C:\Users\LENOVO\Downloads\deliveries.csv")

print(matches.head(5))
print(deliveries.head(5))

matches.shape
matches.info()

deliveries.shape
deliveries.info()

matches['date'] = pd.to_datetime(matches.date)
matches['Season']= matches.date.dt.year
print(matches.head(5))

matches[matches['city'].isna ()]
matches.loc[matches.venue == 'Sharjah Cricket Stadium', 'city'] = 'Sharjah'
matches.loc[matches['city'].isna(), 'city'] = 'Dubai'
matches.info()

matches.loc[matches['winner'].isna(), 'winner'] = 'No Winner'
matches.loc[matches['player_of_match'].isna(), 'player_of_match'] = 'No Player of the Match'
matches.loc[matches['result'].isna(), 'result'] = 'No Result'
matches['result_margin'] = matches['result_margin'].fillna('No Margin').astype(str)
matches.loc[matches['eliminator'].isna(), 'eliminator'] = 'N'
matches.replace('Rising Pune Supergiant', 'Rising Pune Supergiants', inplace=True)
matches.replace('Rising Pune Supergiants', 'Pune Warriors', inplace=True)
matches.replace('Delhi Daredevils', 'Delhi Capitals', inplace=True)

matches.team1.value_counts()

matches.drop('method', axis=1, inplace=True)


matches_played = pd.concat([matches['team1'], matches['team2']])
matches_played = matches_played.value_counts().reset_index()
matches_played.columns = ['Team', 'Total Matches Played']
wins = matches['winner'].value_counts().reset_index()
wins.columns = ['Team', 'Wins']
matches_played = matches_played.merge(wins, on='Team', how='left')
matches_played['winning percentage'] = (matches_played['Wins']/matches_played['Total Matches Played']) * 100

sns.barplot(data=matches_played, x='Team', y='winning percentage')
plt.xticks(rotation=90)
plt.title('Winning Percentage of Teams')
plt.show()

sns.barplot(data=matches_played, x='Team', y='Total Matches Played')
plt.xticks(rotation=90)
plt.title('Total matches played')
plt.show()

sns.barplot(data=matches_played, x='Team', y='Wins')
plt.xticks(rotation=90)
plt.title('Winner of Each Match')
plt.show()

stadium_wise_matches = matches['venue'].value_counts().reset_index()
stadium_wise_matches.columns = ['Stadium', 'Total Matches']

sns.barplot(data=stadium_wise_matches, x='Stadium', y='Total Matches')
plt.xticks(rotation=90)
plt.title('Total Matches Played in Each Stadium')
plt.show()

#how toss affects the match outcome
matches['toss_effect'] = 0

for i in matches.index:
    if matches.toss_winner[i] == matches.winner[i]:
        matches.toss_effect[i] = 1
       
matches.head()

win = matches.groupby(['Season'])['toss_effect'].sum()
total_matches = matches.groupby('Season')['Season'].count()
toss_winner_ratio = np.round((win / total_matches) * 100, decimals=1)
toss_winner_ratio.columns = ['Season', 'percentage']

sns.barplot(x=toss_winner_ratio.index, y=toss_winner_ratio.values)
plt.xticks(rotation=90)
plt.title('Toss Winner Effect on Match Outcome')
plt.xlabel('Season')
plt.ylabel('Percentage of Matches Won by Toss Winner')
plt.show()

toss_wins = matches.groupby('toss_winner')['toss_effect'].count()
toss_winner_matches = matches.groupby('toss_winner')['toss_effect'].sum()

winner_percentage = np.round((toss_winner_matches / toss_wins) * 100, decimals=1).reset_index()
winner_percentage.columns = ['Team', 'Percentage']
winner_percentage = winner_percentage.sort_values(by='Team')

sns.barplot(data=winner_percentage, x='Team', y='Percentage')
plt.xticks(rotation=90)
plt.title('Winning Percentage of Toss Winners')
plt.xlabel('Team')
plt.ylabel('Winning Percentage')
plt.show()

runs = matches.merge(deliveries, how='left')
total_runs_season = runs.groupby('Season')['total_runs'].sum().reset_index()
matches_season = matches.groupby(['Season']).count()["id"].reset_index()
matches_season.rename(columns={'id':'matches'},inplace=True) # here we renamed our column name to matches
matches_season["total_runs"] = total_runs_season["total_runs"]
matches_season["average_runs_per_match"] = matches_season["total_runs"]/ matches_season['matches'] #here we calculated average no. of runs in a season
matches_season.sort_values(by='total_runs' , ascending=False)

sns.barplot(data=matches_season, x='Season', y='average_runs_per_match')
plt.xticks(rotation=90)
plt.title('Average Runs per Match in Each Season')
plt.xlabel('Season')
plt.ylabel('Average Runs')
plt.show()