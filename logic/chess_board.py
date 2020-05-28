from logic.chess_pieces import *
import copy


class Board:

    def __init__(self):
        self.board = {}
        self.half_moves = 0
        self.fifty_moves = 0
        self.white_to_move = True

        for file in range(1, 9):
            for rank in range(1, 9):
                self.board[(file, rank)] = None

        self.white_pieces = [
            Pawn((1, 2), 'white', 'P'),
            Pawn((2, 2), 'white', 'P'),
            Pawn((3, 2), 'white', 'P'),
            Pawn((4, 2), 'white', 'P'),
            Pawn((5, 2), 'white', 'P'),
            Pawn((6, 2), 'white', 'P'),
            Pawn((7, 2), 'white', 'P'),
            Pawn((8, 2), 'white', 'P'),
            Rook((1, 1), 'white', 'R'),
            Rook((8, 1), 'white', 'R'),
            Knight((2, 1), 'white', 'N'),
            Knight((7, 1), 'white', 'N'),
            Bishop((3, 1), 'white', 'B'),
            Bishop((6, 1), 'white', 'B'),
            Queen((4, 1), 'white', 'Q'),
            King((5, 1), 'white', 'K')
        ]

        self.black_pieces = [
            Pawn((1, 7), 'black', 'p'),
            Pawn((2, 7), 'black', 'p'),
            Pawn((3, 7), 'black', 'p'),
            Pawn((4, 7), 'black', 'p'),
            Pawn((5, 7), 'black', 'p'),
            Pawn((6, 7), 'black', 'p'),
            Pawn((7, 7), 'black', 'p'),
            Pawn((8, 7), 'black', 'p'),
            Rook((1, 8), 'black', 'r'),
            Rook((8, 8), 'black', 'r'),
            Knight((2, 8), 'black', 'n'),
            Knight((7, 8), 'black', 'n'),
            Bishop((3, 8), 'black', 'b'),
            Bishop((6, 8), 'black', 'b'),
            Queen((4, 8), 'black', 'q'),
            King((5, 8), 'black', 'k')
        ]
        for white_piece in self.white_pieces:
            self.board[white_piece.square] = white_piece
        for black_piece in self.black_pieces:
            self.board[black_piece.square] = black_piece

        self.prev_state = [copy.deepcopy(self.board)]
        rep = hash(str(self))
        self.threefold_tracker = [rep]

    def __str__(self):
        """Gets a string representation for the board.
        Used mainly for early testing in creating the app"""
        str_board = ""
        for y in range(1, 9):
            str_board += ' ' + str(9-y) + ' |'
            for x in range(1, 9):
                if self.board[(x, 9-y)] is None:
                    str_board += " * "
                else:
                    str_board += ' ' + str(self.board[(x, 9-y)]) + ' '
            str_board += "\n"
        str_board += "    -----------------------\n"
        str_board += "     1  2  3  4  5  6  7  8 "

        return str_board

    def castle_perm(self, king, square):
        """Determines the castleing conditions for the king. Called upon in the .move() method
        and returns the square the king starts on, the square he will move to, the square the
        rook starts on, and the square the rook will move to in a list."""
        castle = None
        if not king.has_moved:
            y = king.square[1]
            if square == (7, y) and self.board[(7, y)] is None and self.board[(6, y)] is None and self.board[(8, y)] is not None and not self.board[(8, y)].has_moved:
                castle = [king.square, (7, y), (8, y), (6, y)]
            elif square == (3, y) and self.board[(3, y)] is None and self.board[(4, y)] is None and self.board[(2, y)] is None and self.board[(1, y)] is not None and  not self.board[(1, y)].has_moved:
                castle = [king.square, (7, y), (8, y), (6, y)]
        return castle

    def king_in_check(self):
        """Returns the king that is currently in check or none if none of the kings are in check"""
        king = None
        all_pieces = []
        for piece in self.board.values():
            if piece is not None:
                all_pieces.append(piece)
        for piece in all_pieces:
            for square in piece.valid_moves(self.board):
                if type(self.board[square]) == King and self.board[square].colour != piece.colour:
                    king = self.board[square]
        return king

    def move(self, sq_one, sq_two):
        """The main function that handles chess moves. This function handles regular captures
        using the .valid_moves method for each piece to see if each move is valid. This function also
        handles en-passent captures, castling, and promotions."""
        piece = self.board[sq_one]

        # en-passent capture
        if type(piece) == Pawn and sq_two == piece.can_en_passent[0] and self.half_moves - 1 == piece.can_en_passent[1]:
            self.fifty_moves = 0
            self.board[sq_two] = self.board[sq_one]
            self.board[sq_one] = None
            self.board[(sq_two[0], sq_one[1])] = None
            piece.square = sq_two
            self.half_moves += 1
            self.white_to_move = not self.white_to_move

        # promotions
        elif type(piece) == Pawn and sq_two in piece.valid_moves(self.board) and sq_two[1] in [8, 1]:
            pro = input("What piece would you like to promote to: ")
            if pro == 'Queen':
                self.board[sq_two] = Queen(sq_two, piece.colour, "Q" if sq_two[1] == 8 else 'q')
            if pro == 'Rook':
                self.board[sq_two] = Rook(sq_two, piece.colour, "R" if sq_two[1] == 8 else 'r')
            if pro == 'Bishop':
                self.board[sq_two] = Bishop(sq_two, piece.colour, "B" if sq_two[1] == 8 else 'b')
            if pro == 'Knight':
                self.board[sq_two] = Knight(sq_two, piece.colour, "N" if sq_two[1] == 8 else 'n')
            self.board[sq_one] = None
            self.half_moves += 1
            self.white_to_move = not self.white_to_move

        # castling
        elif type(piece) == King and self.castle_perm(piece, sq_two) is not None:
            castle_perms = self.castle_perm(piece, sq_two)
            if castle_perms[1] == sq_two:
                r_one = castle_perms[2]
                r_two = castle_perms[3]
                self.board[sq_two] = self.board[sq_one]
                self.board[sq_one] = None
                self.board[r_two] = self.board[r_one]
                self.board[r_one] = None
                piece.square = sq_two
                piece.has_moved = True
                self.board[r_two].square = r_two
                self.board[r_two].has_moved = True
                self.half_moves += 1
                self.white_to_move = not self.white_to_move

        # moving a white piece
        elif self.white_to_move and piece.colour == 'white':
            if sq_two in piece.valid_moves(self.board):
                self.fifty_moves += 1
                # reset fifty move counter
                if self.board[sq_two] is not None or type(piece) == Pawn:
                    self.fifty_moves = 0

                # setting the en-passent conditions of a pawn when the other pawn is pushed two squares
                if type(piece) == Pawn and not piece.has_moved:
                    if abs(sq_two[1] - sq_one[1]) == 2:
                        p_two = self.board[(sq_two[0] + 1, sq_two[1])]
                        if type(p_two) == Pawn and p_two.colour != piece.colour:
                            p_two.can_en_passent = [(sq_two[0], sq_two[1] - 1), self.half_moves]
                        p_two = self.board[(sq_two[0] - 1, sq_two[1])]
                        if type(p_two) == Pawn and p_two.colour != piece.colour:
                            p_two.can_en_passent = [(sq_two[0], sq_two[1] - 1), self.half_moves]

                self.board[sq_two] = self.board[sq_one]
                self.board[sq_one] = None
                piece.square = sq_two
                self.half_moves += 1
                self.white_to_move = not self.white_to_move
                piece.has_moved = True if type(piece) in [King, Rook, Pawn] and not piece.has_moved else True
            else:
                print("Error: The selected piece cannot move there.")

        # moving a black piece
        elif not self.white_to_move and piece.colour == 'black':
            if sq_two in piece.valid_moves(self.board):
                self.fifty_moves += 1
                # reset fifty move counter
                if self.board[sq_two] is not None or type(piece) == Pawn:
                    self.fifty_moves = 0

                # setting the en-passent conditions of a pawn when the other pawn is pushed two squares
                if type(piece) == Pawn and not piece.has_moved:
                    piece.has_moved = True
                    if abs(sq_two[1] - sq_one[1]) == 2:
                        p_two = self.board[(sq_two[0] + 1, sq_two[1])]
                        if type(p_two) == Pawn and p_two.colour != piece.colour:
                            p_two.can_en_passent = [(sq_two[0], sq_two[1] + 1), self.half_moves]
                        p_two = self.board[(sq_two[0] - 1, sq_two[1])]
                        if type(p_two) == Pawn and p_two.colour != piece.colour:
                            p_two.can_en_passent = [(sq_two[0], sq_two[1] + 1), self.half_moves]

                self.board[sq_two] = self.board[sq_one]
                self.board[sq_one] = None
                piece.square = sq_two
                self.half_moves += 1
                self.white_to_move = not self.white_to_move
                piece.has_moved = True if type(piece) in [King, Rook, Pawn] and not piece.has_moved else True
            else:
                print("Error: The selected piece cannot move there.")
        else:
            print("Error: Wrong colour piece selected for move.")

        # check if the move was legal for check
        check = self.king_in_check()
        if check is not None:
            if check.colour != piece.colour:
                print(check.colour + " king is in check!")
                self.add_state(self.board)
            else:
                print("Your king is in check.")
                self.board = self.prev_state[-1]
                self.half_moves -= 1
                self.white_to_move = not self.white_to_move
        else:
            self.add_state(self.board)

    def add_state(self, board):
        b = copy.deepcopy(board)
        self.prev_state.append(b)
        self.prev_state.pop(0)
        rep = hash(str(self))
        self.threefold_tracker.append(rep)

    def game_over(self):
        b = copy.deepcopy(self)
        king = self.king_in_check()
        if self.half_moves != 0 and self.threefold_tracker.count(self.threefold_tracker[-1]) == 3:
            print('draw')
            return True
        if king is None:
            return False
        elif king is not None:
            same_colour = []
            for piece in self.board.values():
                if piece is not None and piece.colour == king.colour:
                    same_colour.append(piece)
            for piece in same_colour:
                for square in piece.valid_moves(b.board):
                    b.board[square] = b.board[piece.square]
                    b.board[piece.square] = None
                    king_two = b.king_in_check()
                    if king_two is None or king_two.colour != piece.colour:
                        return False
            return True
