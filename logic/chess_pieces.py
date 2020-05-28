class Piece:
    def __init__(self, square, colour, rep):
        self.square = square
        self.rep = rep
        self.colour = colour

    def __str__(self):
        return self.rep


class Pawn(Piece):
    def __init__(self, square, colour, rep):
        super().__init__(square, colour, rep)
        self.can_en_passent = [None, None]
        self.has_moved = False
        self.value = 100

    def set_square(self, square):
        self.square = square

    def valid_moves(self, board):
        possible = []
        capture = []
        valid = []

        x = self.square[0]
        y = self.square[1]

        if self.colour == 'white':
            capture.append((x + 1, y + 1))
            capture.append((x - 1, y + 1))
            possible.append((x, y + 1))
            if not self.has_moved:
                possible.append((x, y + 2))
        elif self.colour == 'black':
            capture.append((x + 1, y - 1))
            capture.append((x - 1, y - 1))
            possible.append((x, y - 1))
            if not self.has_moved:
                possible.append((x, y - 2))
        for new in possible:
            if (1 <= new[0] <= 8 and 1 <= new[1] <= 8) and board[new] is None:
                valid.append(new)
        for new in capture:
            if (1 <= new[0] <= 8 and 1 <= new[1] <= 8) and board[new] is not None and board[new].colour != self.colour:
                valid.append(new)
        return valid


class King(Piece):
    def __init__(self, square, colour, rep):
        super().__init__(square, colour, rep)
        self.has_moved = False
        self.in_check = False
        self.value = 50000

    def valid_moves(self, board):
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

        return valid


class Rook(Piece):
    def __init__(self, square, colour, rep):
        super().__init__(square, colour, rep)
        self.has_moved = False
        self.value = 550

    def valid_moves(self, board):
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

        return valid


class Knight(Piece):
    def __init__(self, square, colour, rep):
        super().__init__(square, colour, rep)
        self.value = 325

    def valid_moves(self, board):
        possible = []
        valid = []

        x = self.square[0]
        y = self.square[1]

        possible.append((x+2, y-1))
        possible.append((x+2, y+1))
        possible.append((x-2, y-1))
        possible.append((x-2, y+1))
        possible.append((x+1, y+2))
        possible.append((x-1, y+2))
        possible.append((x+1, y-2))
        possible.append((x-1, y-2))

        for new in possible:
            if (1 <= new[0] <= 8 and 1 <= new[1] <= 8) and (board[new] is None or board[new].colour != self.colour):
                valid.append(new)

        return valid


class Bishop(Piece):
    def __init__(self, square, colour, rep):
        super().__init__(square, colour, rep)
        self.value = 325

    def valid_moves(self, board):
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
                    new = (x, y)
                    break
            else:
                valid.append(new)

        while new[0] - 1 >= 1 and (1 <= l_one(new[0] - 1) <= 8):
            new = (new[0] - 1, l_one(new[0] - 1))
            if board[new] is not None:
                if board[new].colour != self.colour:
                    valid.append(new)
                    break
                else:
                    new = (x, y)
                    break
            else:
                valid.append(new)

        while new[0] + 1 <= 8 and (1 <= l_two(new[0] + 1) <= 8):
            new = (new[0] + 1, l_two(new[0] + 1))
            if board[new] is not None:
                if board[new].colour != self.colour:
                    valid.append(new)
                    break
                else:
                    new = (x, y)
                    break
            else:
                valid.append(new)

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

        return valid


class Queen(Piece):
    def __init__(self, square, colour, rep):
        super().__init__(square, colour, rep)
        self.value = 1000

    def valid_moves(self, board):
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
                    new = (x, y)
                    break
            else:
                valid.append(new)

        while new[0] - 1 >= 1 and (1 <= l_one(new[0] - 1) <= 8):
            new = (new[0] - 1, l_one(new[0] - 1))
            if board[new] is not None:
                if board[new].colour != self.colour:
                    valid.append(new)
                    break
                else:
                    new = (x, y)
                    break
            else:
                valid.append(new)

        while new[0] + 1 <= 8 and (1 <= l_two(new[0] + 1) <= 8):
            new = (new[0] + 1, l_two(new[0] + 1))
            if board[new] is not None:
                if board[new].colour != self.colour:
                    valid.append(new)
                    break
                else:
                    new = (x, y)
                    break
            else:
                valid.append(new)

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

        return valid
