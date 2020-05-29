from app import app
from flask import render_template
from logic.chess_board import Board


@app.route('/')
@app.route('/chess')
def chess():
    # TODO: determine a method of passing the board to a template display
    return render_template('chess.html')
