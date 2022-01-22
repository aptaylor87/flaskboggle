from boggle import Boggle
from flask import Flask, request, render_template, jsonify, session

from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config["SECRET_KEY"] = "supersecret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)
boggle_game = Boggle()

@app.route("/")
def homepage():
    # this generates an instance of the boogle class from boggle.py
    board = boggle_game.make_board()
    # This stores the board in the session
    session['board'] = board
    # adds highscore and nplays to the session handling

    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)
    return render_template("home.html", board=board, highscore=highscore,
                           nplays=nplays)


@app.route("/check-word")
def check_word():
    """Check if word is in dictionary. This route is referenced in the handleSubmit(evt) function in boggle.js """
    word = request.args["word"]
    board = session["board"]
    # this is referencing the bogg_game class instance (defined in boggle.py)
    response = boggle_game.check_valid_word(board, word)
    # The repsonse is wrapped up and returned as json, this gets processed 
    return jsonify({'result': response})

@app.route("/post-score", methods=["POST"])
def post_score():
    """Receive score, update nplays, update high score if appropriate."""

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    session['nplays'] = nplays + 1
    session['highscore'] = max(score, highscore)
    # what is this????? it returns 'brokeRecord' if the score is higher than the highscore?
    return jsonify(brokeRecord=score > highscore)