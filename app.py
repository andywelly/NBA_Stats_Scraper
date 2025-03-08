from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Team codes dictionary
team_codes = {
    "Atlanta Hawks": "ATL",
    "Boston Celtics": "BOS",
    "Brooklyn Nets": "BKN",
    "Charlotte Hornets": "CHA",
    "Chicago Bulls": "CHI",
    "Cleveland Cavaliers": "CLE",
    "Dallas Mavericks": "DAL",
    "Denver Nuggets": "DEN",
    "Detroit Pistons": "DET",
    "Golden State Warriors": "GSW",
    "Houston Rockets": "HOU",
    "Indiana Pacers": "IND",
    "Los Angeles Clippers": "LAC",
    "Los Angeles Lakers": "LAL",
    "Memphis Grizzlies": "MEM",
    "Miami Heat": "MIA",
    "Milwaukee Bucks": "MIL",
    "Minnesota Timberwolves": "MIN",
    "New Orleans Pelicans": "NOP",
    "New York Knicks": "NYK",
    "Oklahoma City Thunder": "OKC",
    "Orlando Magic": "ORL",
    "Philadelphia 76ers": "PHI",
    "Phoenix Suns": "PHX",
    "Portland Trail Blazers": "POR",
    "Sacramento Kings": "SAC",
    "San Antonio Spurs": "SAS",
    "Toronto Raptors": "TOR",
    "Utah Jazz": "UTA",
    "Washington Wizards": "WAS",
}

# Front page route
@app.route("/")
def front_page():
    return render_template("index.html")

# Player stats route
@app.route("/player", methods=["GET", "POST"])
def player():
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
                "player.html",
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

    return render_template("player.html")

# Function to get team names from a game link
def get_teams_from_link(game_url):
    try:
        # Extract team names from the URL
        # Example URL: https://sports.yahoo.com/nba/new-orleans-pelicans-houston-rockets-2025030810/
        parts = game_url.split("/")
        teams_part = parts[-2]  # Get the part like "new-orleans-pelicans-houston-rockets-2025030810"
        teams = teams_part.split("-")[:-1]  # Remove the date part

        # Determine the number of parts for each team
        # Try 3 parts first for the first team
        team1 = None
        team2 = None

        # Try 3 parts for the first team
        if len(teams) >= 3:
            team1_candidate = " ".join(teams[:3])  # First team (e.g., "new orleans pelicans")
            if team1_candidate.title() in team_codes:
                team1 = team1_candidate
                remaining_teams = teams[3:]  # Remaining parts for the second team
            else:
                # Fallback to 2 parts for the first team
                team1_candidate = " ".join(teams[:2])  # First team (e.g., "houston rockets")
                if team1_candidate.title() in team_codes:
                    team1 = team1_candidate
                    remaining_teams = teams[2:]  # Remaining parts for the second team

        # Try 3 parts for the second team
        if len(remaining_teams) >= 3:
            team2_candidate = " ".join(remaining_teams[:3])  # Second team (e.g., "houston rockets")
            if team2_candidate.title() in team_codes:
                team2 = team2_candidate
            else:
                # Fallback to 2 parts for the second team
                team2_candidate = " ".join(remaining_teams[:2])  # Second team (e.g., "houston rockets")
                if team2_candidate.title() in team_codes:
                    team2 = team2_candidate
        else:
            # Second team has 2 parts
            team2_candidate = " ".join(remaining_teams[:2])  # Second team (e.g., "houston rockets")
            if team2_candidate.title() in team_codes:
                team2 = team2_candidate

        return team1.title(), team2.title()  # Convert to title case
    except Exception as e:
        print(f"Error parsing {game_url}: {e}")
        return None, None

# Function to generate Basketball Reference links
def get_basketball_reference_links(team1_code, team2_code, year=2025):
    base_url = "https://www.basketball-reference.com/teams"
    team1_link = f"{base_url}/{team1_code}/{year}.html"
    team2_link = f"{base_url}/{team2_code}/{year}.html"
    return team1_link, team2_link

# Games route
@app.route("/games")
def games():
    # Fetch the page
    page = requests.get("https://sports.yahoo.com/nba/scoreboard/?confId=&dateRange=2025-03-09")
    soup = BeautifulSoup(page.text, "html.parser")

    # Find all game links
    games = soup.find_all("a", class_="gamecard-pregame")

    # Extract href attributes
    game_links = []
    for game in games:
        href = game.get("href")  # Get the href attribute
        if href:
            full_url = f"https://sports.yahoo.com{href}"  # Construct the full URL
            game_links.append(full_url)

    # Extract team names and generate Basketball Reference links
    games_teams = []
    for link in game_links:
        team1, team2 = get_teams_from_link(link)
        if team1 and team2:
            team1_code = team_codes.get(team1, "UNK")  # Get team code or "UNK" if not found
            team2_code = team_codes.get(team2, "UNK")  # Get team code or "UNK" if not found

            # Generate Basketball Reference links
            team1_link, team2_link = get_basketball_reference_links(team1_code, team2_code)

            # Store the results
            games_teams.append({
                "game_url": link,
                "team1": team1,
                "team1_code": team1_code,
                "team1_link": team1_link,
                "team2": team2,
                "team2_code": team2_code,
                "team2_link": team2_link,
            })

    # Render the games template with the data
    return render_template("games.html", games_teams=games_teams)

if __name__ == "__main__":
    app.run(debug=True)