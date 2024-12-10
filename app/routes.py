from flask import render_template, request, redirect, url_for
from app import app
from game import Game

g = Game()

@app.route('/')
def index():
    return render_template('index.html', current_player=g.board.to_move)

@app.route('/play', methods=['POST'])
def play():
    pass

@app.route('/get_board', methods=['GET'])
def get_board():
    pass

@app.route('/reset', methods=['POST'])
def reset():
    g = Game()
