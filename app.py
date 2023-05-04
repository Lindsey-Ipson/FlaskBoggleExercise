from flask import Flask, request, render_template, jsonify, session
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ImASecretKey'

boggle_game = Boggle()

@app.route('/')
def homepage():
    """Show homepage with gameboard"""
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get('highscore', 'N/A')
    num_plays = session.get('num_plays', 0)

    return render_template('index.html', board=board, highscore=highscore, num_plays=num_plays)

@app.route('/check-guess')
def check_guess():
    """Check if word is in dictionary"""

    guess = request.args["guess"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, guess)

    return jsonify({'result': response})

@app.route('/end-game', methods=['POST'])
def end_game():
    """Get score, update number of plays, and update high score if needed"""

    score = request.json['score']
    highscore = session.get('highscore', 0)
    num_plays = session.get('num_plays', 0)

    session['num_plays'] = num_plays + 1
    session['highscore'] = max(highscore, score)
    
    return jsonify(newRecord = score > highscore)
