from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_url = request.form.get("user_url")
        market_request = request.form.get("market_request")

        if not user_url.startswith("https://www.basketball-reference.com/players"):
            return "Invalid URL. Should start with: https://www.basketball-reference.com/players"

        try:
            page = requests.get(user_url)
            soup = BeautifulSoup(page.text, 'lxml')

            table = soup.find('table', class_="stats_table")
            if not table:
                return "Stats table not found on the page."

            tbody = table.find('tbody')
            games = tbody.find_all('tr')

            name = soup.find('h1').text.strip()
            team = games[0].find_all('td')[0].find('a').text.strip()

            points = [game.find_all('td')[23].text.strip() for game in games]
            assists = [game.find_all('td')[18].text.strip() for game in games]
            rebounds = [game.find_all('td')[17].text.strip() for game in games]
            steals = [game.find_all('td')[19].text.strip() for game in games]
            blocks = [game.find_all('td')[20].text.strip() for game in games]
            turnovers = [game.find_all('td')[21].text.strip() for game in games]
            threePM = [game.find_all('td')[9].text.strip() for game in games]

            return render_template(
                "results.html",
                name=name,
                team=team,
                points=points,
                assists=assists,
                rebounds=rebounds,
                steals=steals,
                blocks=blocks,
                turnovers=turnovers,
                threePM=threePM,
                market_request=market_request,
            )

        except Exception as e:
            return f"An error occurred: {str(e)}"

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)