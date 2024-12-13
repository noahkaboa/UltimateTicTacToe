from flask import render_template, request, redirect, url_for
from app import app
from game import BigBoard
import json
from werkzeug.datastructures import ImmutableMultiDict

game = BigBoard()

@app.route('/')
def index():
    return render_template('index.html', current_player=game.to_move)

@app.route('/play', methods=['POST'])
def play():

    data = json.loads(list(request.form.to_dict(flat=False).keys())[0])['data'] #Surely better way to do this

    response = {
        "success": False,
        "player": game.to_move,
    }

    big_row = data['big_row']
    big_col = data['big_col']
    small_row = data['small_row']
    small_col = data['small_col']

    print(big_row, big_col, small_row, small_col)


    if game.make_move(int(big_row), int(big_col), int(small_row), int(small_col)):
        response["success"] = True
        response["message"] = "Move successful"
        return json.dumps(response)
    else:
        response["success"] = False
        response["message"] = "Invalid move"
        return json.dumps(response)

    

@app.route('/get_board', methods=['GET'])
def get_board():
    pass

@app.route('/reset', methods=['POST'])
def reset():
    global game
    game = BigBoard()
    return redirect(url_for('index'))

