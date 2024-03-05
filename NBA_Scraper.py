import pandas as pd
import requests
pd.set_option('display.max_columns', None)
import time
import numpy as np

test_url = 'https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=PerGame&Scope=S&Season=2023-24&SeasonType=Regular%20Season&StatCategory=PTS'

r = requests.get(url=test_url).json()

games_url = 'https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json'

games_data = requests.get(url=games_url).json()

games_list = games_data['scoreboard']['games']

for game in games_list:
    home_team_name = game['homeTeam']['teamName']
    away_team_name = game['awayTeam']['teamName']
    game_time_et = game['gameEt']
    
    print(f"{home_team_name} V {away_team_name} at {game_time_et}")