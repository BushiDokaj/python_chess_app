# used to test logic code for any bugs found.
from logic.chess_board import Board

b=Board()
b.move((5,2),(5,4))
b.move((5,7),(5,5))
b.move((6,1),(3,4))
print(b)