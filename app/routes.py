from app import app
from flask import render_template, request, jsonify, make_response, redirect, url_for, session
import pickle
from uuid import uuid4
from logic.chess_board import Board
from logic.chess_pieces import *
from cachelib.simple import SimpleCache

c = SimpleCache()


@app.route('/', methods=["GET", "POST"])
@app.route('/chess', methods=["GET", "POST"])
def chess():
    b = load_board()

    flipped = b.flipped
    img_dict = b.board_html()

    save_board(b)

    return render_template('base.html', img_dict=img_dict, flipped=flipped)


@app.route('/flip')
def flip():
    b = load_board()

    b.flipped = not b.flipped

    save_board(b)

    return redirect(url_for('chess'))


@app.route('/new_game', methods=["GET", "POST"])
def new_game():
    b = load_board()

    b.reset()

    save_board(b)

    return redirect(url_for('chess'))


@app.route('/moves', methods=["POST"])
def load_moves():
    b = load_board()

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
    b = load_board()

    error = False

    sq_one = eval(request.get_json()['sq_one'])
    sq_two = eval(request.get_json()['sq_two'])
    promotion = request.get_json()['promotion']

    try:
        b.move(sq_one, sq_two, promotion)
        save_board(b)
    except Exception as e:
        error = str(e)

    return make_response(jsonify(error))


@app.route('/execute', methods=['GET', 'POST'])
def execute():
    b = load_board()

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
            save_board(b)
        except Exception as e:
            error = str(e)
        response = {'error': error, 'castle': castle, 'empty': empty, 'outcome': outcome}

    return make_response(jsonify(response))


def generate_id():
    return uuid4().__str__()


def load_board():

    if 'game_id' in session and c.get(session['game_id']) is not None:
        pb = c.get(session['game_id'])
        board = pickle.loads(pb)
    else:
        # Initialize new board
        board = Board()

    return board


def save_board(board):
    pb = pickle.dumps(board)

    if 'game_id' in session:
        c.set(session['game_id'], pb)
    else:
        unique_id = generate_id()
        session['game_id'] = unique_id
        c.set(unique_id, pb)
