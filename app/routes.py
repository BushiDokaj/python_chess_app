from app import app
from flask import render_template, request, jsonify, make_response
from logic.chess_board import Board

b = Board()


@app.route('/', methods=["GET", "POST"])
def chess():
    req = request.get_json()

    if request.method == 'POST' and req is not None and b.board[eval(req['sq_one'])] is not None:
        b.move(eval(req['sq_one']), eval(req['sq_two']))
        img_dict = b.board_to_img()
        return render_template('chess.html', img_dict=img_dict)
    else:
        img_dict = b.board_to_img()
        return render_template('chess.html', img_dict=img_dict)
