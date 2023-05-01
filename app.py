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


    return render_template('index.html', board=board)


