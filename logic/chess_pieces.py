from copy import deepcopy


class Piece:
    def __init__(self, square, colour, rep):
        self.square = square
        self.rep = rep
        self.colour = colour
        self.moves = []

    def __str__(self):
        return self.rep

    def remove_moves_for_check(self, board):
        p_moves = self.moves[:]

        for move in p_moves:
            b = deepcopy(board)
            if b.board[move] is not None:
                b.remove_piece(move)
            b.board[move] = b.board[self.square]
            b.board[self.square] = None
            b.update_moves(remove=False)
            if self.colour == 'white':
                for p in b.black_pieces:
                    p.update_valid_moves(b, remove=False)
                    con = False
                    for square in p.moves:
                        if type(b.board[square]) == King:
                            self.moves.remove(move)
                            con = True
                            break
                    if con:
                        break
            else:
                for p in b.white_pieces:
                    p.update_valid_moves(b, remove=False)
                    con = False
                    for square in p.moves:
                        if type(b.board[square]) == King:
                            self.moves.remove(move)
                            con = True
                            break
                    if con:
                        break


class Pawn(Piece):
    def __init__(self, square, colour, rep):
        super().__init__(square, colour, rep)
        self.can_en_passent = [None, None]
        self.has_moved = False
        self.value = 100
        self.img = self.colour + "_pawn.png"

    def set_square(self, square):
        self.square = square

    def update_valid_moves(self, b, remove=True):
        board = b.board
        possible = []
        capture = []
        valid = []

        x = self.square[0]
        y = self.square[1]

        if self.colour == 'white':
            capture.append((x + 1, y + 1))
            capture.append((x - 1, y + 1))
            possible.append((x, y + 1))
            if not self.has_moved and board[(x, y+1)] is None:
                possible.append((x, y + 2))
        elif self.colour == 'black':
            capture.append((x + 1, y - 1))
            capture.append((x - 1, y - 1))
            possible.append((x, y - 1))
            if not self.has_moved and board[(x, y-1)] is None:
                possible.append((x, y - 2))
        for new in possible:
            if (1 <= new[0] <= 8 and 1 <= new[1] <= 8) and board[new] is None:
                valid.append(new)
        for new in capture:
            if (1 <= new[0] <= 8 and 1 <= new[1] <= 8) and board[new] is not None and board[new].colour != self.colour:
                valid.append(new)

        if self.can_en_passent[0] is not None and self.can_en_passent[1] == (b.half_moves - 1):
            valid.append(self.can_en_passent[0])

        self.moves = valid

        if remove:
            self.remove_moves_for_check(b)


class King(Piece):
    def __init__(self, square, colour, rep):
        super().__init__(square, colour, rep)
        self.has_moved = False
        self.in_check = False
        self.value = 50000
        self.img = self.colour + "_king.png"
        self.castle = {'king_side': None, 'queen_side': None}

    def castle_perm(self, board, x, y):
        """Determines the castleing conditions for the king. Called upon in the .move() method
        and returns the square the king starts on, the square he will move to, the square the
        rook starts on, and the square the rook will move to in a list."""
        perm = True

        for piece in board.values():
            if piece is not None and piece.colour != self.colour:
                if (x-1, y) in piece.moves or (x, y) in piece.moves:
                    perm = False
                    break

        return perm

    def castling(self, board):
        y = self.square[1]

        if board[(7, y)] is None and board[(6, y)] is None and board[(8, y)] is not None and type(board[(8, y)]) == Rook and not board[(8, y)].has_moved and not self.in_check and self.castle_perm(board, 7, y):
            self.moves.append((7, y))
            self.castle['king_side'] = (7, y)
        else:
            self.castle['king_side'] = None

        if board[(3, y)] is None and board[(4, y)] is None and board[(2, y)] is None and board[(1, y)] is not None and type(board[(1, y)]) == Rook and not board[(1, y)].has_moved and not self.in_check and self.castle_perm(board, 4, y):
            self.moves.append((3, y))
            self.castle['queen_side'] = (3, y)
        else:
            self.castle['queen_side'] = None

    def update_valid_moves(self, b, remove=True):
        board = b.board
        possible = []
        valid = []

        x = self.square[0]
        y = self.square[1]

        possible.append((x + 1, y + 1))
        possible.append((x - 1, y + 1))
        possible.append((x + 1, y - 1))
        possible.append((x, y + 1))
        possible.append((x + 1, y))
        possible.append((x, y - 1))
        possible.append((x - 1, y))
        possible.append((x - 1, y - 1))

        for new in possible:
            if (1 <= new[0] <= 8 and 1 <= new[1] <= 8) and (board[new] is None or board[new].colour != self.colour):
                valid.append(new)

        self.moves = valid

        if remove:
            self.remove_moves_for_check(b)

        self.castling(board)


class Rook(Piece):
    def __init__(self, square, colour, rep):
        super().__init__(square, colour, rep)
        self.has_moved = False
        self.value = 550
        self.img = self.colour + "_rook.png"

    def update_valid_moves(self, b, remove=True):
        board = b.board
        valid = []

        x = self.square[0]
        y = self.square[1]

        for i in range(1, x):
            new = (x - i, y)
            if board[new] is not None:
                if board[new].colour != self.colour:
                    valid.append(new)
                    break
                else:
                    break
            else:
                valid.append(new)

        for i in range(x + 1, 9):
            new = (i, y)
            if board[new] is not None:
                if board[new].colour != self.colour:
                    valid.append(new)
                    break
                else:
                    break
            else:
                valid.append(new)

        for i in range(1, y):
            new = (x, y - i)
            if board[new] is not None:
                if board[new].colour != self.colour:
                    valid.append(new)
                    break
                else:
                    break
            else:
                valid.append(new)

        for i in range(y + 1, 9):
            new = (x, i)
            if board[new] is not None:
                if board[new].colour != self.colour:
                    valid.append(new)
                    break
                else:
                    break
            else:
                valid.append(new)

        self.moves = valid

        if remove:
            self.remove_moves_for_check(b)


class Knight(Piece):
    def __init__(self, square, colour, rep):
        super().__init__(square, colour, rep)
        self.value = 325
        self.img = self.colour + "_knight.png"

    def update_valid_moves(self, b, remove=True):
        board = b.board
        possible = []
        valid = []

        x = self.square[0]
        y = self.square[1]

        possible.append((x + 2, y - 1))
        possible.append((x + 2, y + 1))
        possible.append((x - 2, y - 1))
        possible.append((x - 2, y + 1))
        possible.append((x + 1, y + 2))
        possible.append((x - 1, y + 2))
        possible.append((x + 1, y - 2))
        possible.append((x - 1, y - 2))

        for new in possible:
            if (1 <= new[0] <= 8 and 1 <= new[1] <= 8) and (board[new] is None or board[new].colour != self.colour):
                valid.append(new)

        self.moves = valid

        if remove:
            self.remove_moves_for_check(b)


class Bishop(Piece):
    def __init__(self, square, colour, rep):
        super().__init__(square, colour, rep)
        self.value = 325
        self.img = self.colour + "_bish.png"

    def update_valid_moves(self, b, remove=True):
        board = b.board
        valid = []

        x = self.square[0]
        y = self.square[1]
        new = (x, y)

        l_one = lambda a: a - x + y
        l_two = lambda b: -b + x + y

        while new[0] + 1 <= 8 and (1 <= l_one(new[0] + 1) <= 8):
            new = (new[0] + 1, l_one(new[0] + 1))
            if board[new] is not None:
                if board[new].colour != self.colour:
                    valid.append(new)
                    break
                else:
                    break
            else:
                valid.append(new)

        new = (x, y)

        while new[0] - 1 >= 1 and (1 <= l_one(new[0] - 1) <= 8):
            new = (new[0] - 1, l_one(new[0] - 1))
            if board[new] is not None:
                if board[new].colour != self.colour:
                    valid.append(new)
                    break
                else:
                    break
            else:
                valid.append(new)

        new = (x, y)

        while new[0] + 1 <= 8 and (1 <= l_two(new[0] + 1) <= 8):
            new = (new[0] + 1, l_two(new[0] + 1))
            if board[new] is not None:
                if board[new].colour != self.colour:
                    valid.append(new)
                    break
                else:
                    break
            else:
                valid.append(new)

        new = (x, y)

        while new[0] - 1 >= 1 and (1 <= l_two(new[0] - 1) <= 8):
            new = (new[0] - 1, l_two(new[0] - 1))
            if board[new] is not None:
                if board[new].colour != self.colour:
                    valid.append(new)
                    break
                else:
                    break
            else:
                valid.append(new)

        self.moves = valid

        if remove:
            self.remove_moves_for_check(b)


class Queen(Piece):
    def __init__(self, square, colour, rep):
        super().__init__(square, colour, rep)
        self.value = 1000
        self.img = self.colour + "_queen.png"

    def update_valid_moves(self, b, remove=True):
        board = b.board
        valid = []

        x = self.square[0]
        y = self.square[1]

        for i in range(1, x):
            new = (x - i, y)
            if board[new] is not None:
                if board[new].colour != self.colour:
                    valid.append(new)
                    break
                else:
                    break
            else:
                valid.append(new)

        for i in range(x + 1, 9):
            new = (i, y)
            if board[new] is not None:
                if board[new].colour != self.colour:
                    valid.append(new)
                    break
                else:
                    break
            else:
                valid.append(new)

        for i in range(1, y):
            new = (x, y - i)
            if board[new] is not None:
                if board[new].colour != self.colour:
                    valid.append(new)
                    break
                else:
                    break
            else:
                valid.append(new)

        for i in range(y + 1, 9):
            new = (x, i)
            if board[new] is not None:
                if board[new].colour != self.colour:
                    valid.append(new)
                    break
                else:
                    break
            else:
                valid.append(new)

        new = (x, y)

        l_one = lambda a: a - x + y
        l_two = lambda b: -b + x + y

        while new[0] + 1 <= 8 and (1 <= l_one(new[0] + 1) <= 8):
            new = (new[0] + 1, l_one(new[0] + 1))
            if board[new] is not None:
                if board[new].colour != self.colour:
                    valid.append(new)
                    break
                else:
                    break
            else:
                valid.append(new)

        new = (x, y)

        while new[0] - 1 >= 1 and (1 <= l_one(new[0] - 1) <= 8):
            new = (new[0] - 1, l_one(new[0] - 1))
            if board[new] is not None:
                if board[new].colour != self.colour:
                    valid.append(new)
                    break
                else:
                    break
            else:
                valid.append(new)

        new = (x, y)

        while new[0] + 1 <= 8 and (1 <= l_two(new[0] + 1) <= 8):
            new = (new[0] + 1, l_two(new[0] + 1))
            if board[new] is not None:
                if board[new].colour != self.colour:
                    valid.append(new)
                    break
                else:
                    break
            else:
                valid.append(new)

        new = (x, y)

        while new[0] - 1 >= 1 and (1 <= l_two(new[0] - 1) <= 8):
            new = (new[0] - 1, l_two(new[0] - 1))
            if board[new] is not None:
                if board[new].colour != self.colour:
                    valid.append(new)
                    break
                else:
                    break
            else:
                valid.append(new)

        self.moves = valid

        if remove:
            self.remove_moves_for_check(b)
