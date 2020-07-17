from app import app
from flask import render_template, request, jsonify, make_response, redirect, url_for
from logic.chess_board import Board
from logic.chess_pieces import *

b = Board()

@app.route('/', methods=["GET", "POST"])
@app.route('/chess', methods=["GET", "POST"])
def chess():
    flipped = b.flipped

    img_dict = b.board_html()

    return render_template('base.html', img_dict=img_dict, flipped=flipped)


@app.route('/flip')
def flip():
    b.flipped = not b.flipped
    return redirect(url_for('chess'))


@app.route('/new_game', methods=["GET", "POST"])
def new_game():
    b.reset()
    return redirect(url_for('chess'))


@app.route('/moves', methods=["POST"])
def load_moves():
    moves = []
    if request.method == 'POST':
        sq = request.get_json()['sq_one']
        piece = b.board[eval(sq)]
        if (b.white_to_move and piece.colour == 'white') or (not b.white_to_move and piece.colour == 'black'):
            moves = b.board[eval(sq)].moves
        else:
            raise Exception('Wrong colour piece selected for move')

    return make_response(jsonify(moves))


@app.route('/promote', methods=['GET', 'POST'])
def promote():
    error = False

    sq_one = eval(request.get_json()['sq_one'])
    sq_two = eval(request.get_json()['sq_two'])
    promotion = request.get_json()['promotion']

    try:
        b.move(sq_one, sq_two, promotion)
    except Exception as e:
        error = str(e)

    return make_response(jsonify(error))


@app.route('/execute', methods=['GET', 'POST'])
def execute():
    if request.method == "POST":

        castle = None
        error = False
        outcome = False
        empty = None

        sq_one = eval(request.get_json()['sq_one'])
        sq_two = eval(request.get_json()['sq_two'])
        piece = b.board[sq_one]

        if type(piece) == King and (piece.castle['king_side'] == sq_two or piece.castle['queen_side'] == sq_two):
            y = sq_one[1]
            if piece.castle['king_side'] == sq_two:
                r_one = str((8, y))
                r_two = str((6, y))

            elif piece.castle['queen_side'] == sq_two:
                r_one = str((1, y))
                r_two = str((4, y))
            castle = [r_one, r_two]

        try:
            b.move(sq_one, sq_two)
            if b.game_over():
                outcome = b.outcome
            empty = b.js_remove()
        except Exception as e:
            error = str(e)
        response = {'error': error, 'castle': castle, 'empty': empty, 'outcome': outcome}

    return make_response(jsonify(response))
