from app import app
from logic.chess_board import Board


@app.route('/')
@app.route('/chess')
def chess():
    # TODO: determine a method of passing the board to a template display
    pass
