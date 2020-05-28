from logic.chess_board import Board

b = Board()
print(b)
while not b.game_over():

    print("\n")
    x_one = int(input("x one: "))
    y_one = int(input("y one: "))
    sq_one = (x_one, y_one)
    if b.board[sq_one] is None:
        print("You must select a square with a piece!")
        continue
    x_two = int(input("x two: "))
    y_two = int(input("x two: "))
    sq_two = (x_two, y_two)
    b.move(sq_one, sq_two)
    print(b)
    print('\n')
