# used to test logic code for any bugs found.
from logic.chess_board import Board

b=Board()
b.move((5,2),(5,4))
b.move((5,7),(5,5))
b.move((4,1),(8,5))
b.move((6,7),(6,6))
print(b)