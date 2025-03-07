from flask import Flask, render_template

app = Flask(__name__)

# Register blueprints
from player.routes import player_bp
from games.routes import games_bp

app.register_blueprint(player_bp, url_prefix="/player")
app.register_blueprint(games_bp, url_prefix="/games")

@app.route("/")
def front_page():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)