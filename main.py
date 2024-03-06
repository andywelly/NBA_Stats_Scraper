from bs4 import BeautifulSoup
import requests
import sys



POINT_MARKETS = [5, 10, 15, 20, 25, 30, 35]


def point_odds(point_array):
    for market in POINT_MARKETS:
        print("Market: " + str(market) + "+ Points")
        winning_odds = check_market_hit(point_array, market)
        print("Minimum Winning Odds" + str(winning_odds) + "\n")
    
        
            
def check_market_hit(stat_array, market):
    count = 0;
    for stat in stat_array:
        if (int(stat) >= market):
            count += 1
    hit_rate = (count / 5)
    odds = 1 / hit_rate
    return odds


print("\nEnter player statistic url from basketball reference")
print("Should be in the form: https://www.basketball-reference.com/players/...\n")


user_url = input("Enter URL: ")

if (user_url.startswith("https://www.basketball-reference.com/players")):
    print("\nRetrieving statistics for:");
else:
    sys.exit("Invalid URL\nShould start with: https://www.basketball-reference.com/players")


page = requests.get(user_url)
soup = BeautifulSoup(page.text, 'lxml')

name = soup.find('h1').text;
print(name)

table = soup.find('table', class_="stats_table")
tbody = table.find('tbody')
games = tbody.find_all('tr')

points = []
assists = []
rebounds = []
steals = []
blocks = []
turnovers = []
threePM = []

for game in games:
    stats = game.find_all('td')
    points.append(stats[23].text)
    assists.append(stats[18].text)
    rebounds.append(stats[17].text)
    steals.append(stats[19].text)
    blocks.append(stats[20].text)
    turnovers.append(stats[21].text)
    threePM.append(stats[9].text)

point_odds(points)



