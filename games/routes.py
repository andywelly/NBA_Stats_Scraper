from flask import Blueprint, render_template

# Create a Blueprint for games routes and specify the template folder
games_bp = Blueprint("games", __name__, template_folder="templates")

@games_bp.route("/")
def games():
    return render_template("games.html")  # Look for games.html in the games/templates folder