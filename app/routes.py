from flask import render_template, request, redirect, url_for
from app import app
from game import BigBoard
import json
from werkzeug.datastructures import ImmutableMultiDict

game = BigBoard()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game')
def game_page():
    return render_template('game.html', current_player=game.to_move)

@app.route('/play', methods=['POST', 'GET'])
def play():
    if request.method == 'GET':
        return redirect(url_for('fourofour'))

    if request.method == 'POST':
        data = json.loads(list(request.form.to_dict(flat=False).keys())[0])['data'] #Surely better way to do this

        response = {
            "success": False,
            "player": game.to_move,
        }

        big_row = data['big_row']
        big_col = data['big_col']
        small_row = data['small_row']
        small_col = data['small_col']

        if game.make_move(int(big_row), int(big_col), int(small_row), int(small_col)):
            response["success"] = True
            response["message"] = "Move successful"
            response["wins"] = game.big_board[int(big_row)][int(big_col)].check_winner()
            valid_moves = []
            for big_row in range(3):
                for big_col in range(3):
                    for small_row in range(3):
                        for small_col in range(3):
                            if game.is_valid_move(big_row, big_col, small_row, small_col):
                                valid_moves.append([big_row, big_col, small_row, small_col, "possible"])
                            else:
                                valid_moves.append([big_row, big_col, small_row, small_col, ""])
            response["valid_moves"] = valid_moves

            response["utn"] = game.board_to_utn()

            response["game_over"] = game.game_state.check_winner()
                            
            return json.dumps(response)
        else:
            response["success"] = False
            response["message"] = "Invalid move"
            return json.dumps(response)

    

@app.route('/reset', methods=['POST', 'GET'])
def reset():
    global game
    game = BigBoard()
    return redirect(url_for('game_page'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/404')
def fourofour():
    return render_template('404.html')

@app.route('/set-utn', methods=['GET', 'POST'])
def set_utn():
    if request.method == 'GET':
        return redirect(url_for('fourofour'))
    data = request.form.to_dict(flat=False)
    print(data)
    utn = data['utn'][0]
    game.utn_to_board(utn)
    valid_moves = []
    for big_row in range(3):
        for big_col in range(3):
            for small_row in range(3):
                for small_col in range(3):
                    if game.is_valid_move(big_row, big_col, small_row, small_col):
                        valid_moves.append([big_row, big_col, small_row, small_col, "possible"])
                    else:
                        valid_moves.append([big_row, big_col, small_row, small_col, ""])
    
    return_data = {
        "valid_moves": valid_moves,
        "expanded_utn": game.utn_parse(utn),
        "player": game.to_move
    }
    
    return json.dumps(return_data)