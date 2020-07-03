# used to test logic code for any bugs found.
from logic.chess_board import Board

b=Board()
b.move((5,2),(5,4))
b.move((5,7),(5,5))
b.move((6,1),(5,2))
b.move((6,8),(5,7))
b.move((7,1),(6,3))
b.move((7,8),(6,6))
b.move((5,1),(7,1))
b.move(())
print(b)