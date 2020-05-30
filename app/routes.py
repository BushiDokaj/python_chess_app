from app import app
from flask import render_template
from logic.chess_board import Board


@app.route('/')
@app.route('/chess')
def chess():
    b = Board()
    img_dict = b.board_to_img()
    return render_template('chess.html', img_dict=img_dict)
