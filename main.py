from bs4 import BeautifulSoup
import requests
import sys
import markets
import odds

# Arrays to store player stat vales
points = []
assists = []
rebounds = []
steals = []
blocks = []
turnovers = []
threePM = []


# Request for user input
print("\nEnter player statistic url from basketball reference")
print("Should be in the form: https://www.basketball-reference.com/players/...\n")
user_url = input("Enter URL: ")


# Validates user input to be in proper form
if (user_url.startswith("https://www.basketball-reference.com/players")):
    print("\nRetrieving statistics");
else:
    sys.exit("Invalid URL\nShould start with: https://www.basketball-reference.com/players")

market_request = input("Enter Market: ")

print("Retrieveing " + market_request)


# Using BeautifulSoup to scrape html file from basketball reference
page = requests.get(user_url)
soup = BeautifulSoup(page.text, 'lxml')


table = soup.find('table', class_="stats_table")
tbody = table.find('tbody')
games = tbody.find_all('tr')


name = soup.find('h1').text;
team = games[0].find_all('td')[0].find('a').text
print(name + team + "\n")


for game in games:
    stats = game.find_all('td')
    points.append(stats[23].text)
    assists.append(stats[18].text)
    rebounds.append(stats[17].text)
    steals.append(stats[19].text)
    blocks.append(stats[20].text)
    turnovers.append(stats[21].text)
    threePM.append(stats[9].text)


#odds.check_odds(points, markets.POINT_MARKETS, "points")
#odds.check_odds(assists, markets.ASSIST_MARKETS, "assists")

print(points)
print(assists)
print(rebounds)
print(threePM)


