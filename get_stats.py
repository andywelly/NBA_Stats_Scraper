from bs4 import BeautifulSoup
import requests
import sys

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



print(points)
print(assists)
print(rebounds)
print(steals)
print(blocks)
print(turnovers)
print(threePM)
print("\n")