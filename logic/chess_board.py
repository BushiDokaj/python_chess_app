from logic.chess_pieces import *
import copy


class Board:

    def __init__(self):
        self.board = {}
        self.half_moves = 0
        self.fifty_moves = 0
        self.white_to_move = None
        self.white_pieces = []
        self.black_pieces = []
        self.prev_state = []
        self.threefold_tracker = []
        self.flipped = False
        self.outcome = None
        self.reset()

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

    def reset(self):
        self.half_moves = 0
        self.fifty_moves = 0
        self.white_to_move = True
        self.flipped = False
        self.outcome = None

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

        # initiate the valid moves for each piece at the start
        self.update_moves()

    def king_in_check(self):
        """Returns the king that is currently in check or none if none of the kings are in check"""
        king = None
        if self.white_to_move:
            for piece in self.black_pieces:
                for square in piece.moves:
                    if type(self.board[square]) == King:
                        king = self.board[square]
        else:
            for piece in self.white_pieces:
                for square in piece.moves:
                    if type(self.board[square]) == King:
                        king = self.board[square]
        return king

    def move(self, sq_one, sq_two, promotion=None):
        """The main function that handles chess moves. This function handles regular captures
        using the .valid_moves method for each piece to see if each move is valid. This function also
        handles en-passent captures, castling, and promotions."""

        piece = self.board[sq_one]
        print(piece)

        # en-passent capture
        if type(piece) == Pawn and sq_two == piece.can_en_passent[0] and self.half_moves - 1 == piece.can_en_passent[1]:
            self.fifty_moves = 0
            self.board[sq_two] = self.board[sq_one]
            self.board[sq_one] = None
            self.remove_piece((sq_two[0], sq_one[1]))
            self.board[(sq_two[0], sq_one[1])] = None
            piece.square = sq_two
            self.half_moves += 1
            self.white_to_move = not self.white_to_move

        elif promotion is not None and type(piece) == Pawn and sq_two in piece.moves and sq_two[1] in[8, 1]:
            if self.board[sq_two] is not None:
                self.remove_piece(sq_two)

            if promotion == 'q':
                self.board[sq_two] = Queen(sq_two, piece.colour, "Q" if sq_two[1] == 8 else 'q')
            elif promotion == 'r':
                self.board[sq_two] = Rook(sq_two, piece.colour, "R" if sq_two[1] == 8 else 'r')
            elif promotion == 'b':
                self.board[sq_two] = Bishop(sq_two, piece.colour, "B" if sq_two[1] == 8 else 'b')
            elif promotion == 'n':
                self.board[sq_two] = Knight(sq_two, piece.colour, "N" if sq_two[1] == 8 else 'n')

            self.remove_piece(sq_one)
            self.board[sq_one] = None

            new = self.board[sq_two]
            if new.colour == 'white':
                self.white_pieces.append(new)
            else:
                self.black_pieces.append(new)

            self.half_moves += 1
            self.white_to_move = not self.white_to_move

        # castling
        elif type(piece) == King and (piece.castle['king_side'] == sq_two or piece.castle['queen_side'] == sq_two):
            y = sq_one[1]

            if piece.castle['king_side'] == sq_two:
                r_one = (8, y)
                r_two = (6, y)

            elif piece.castle['queen_side'] == sq_two:
                r_one = (1, y)
                r_two = (4, y)

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
            if sq_two in piece.moves:
                self.fifty_moves += 1
                # reset fifty move counter
                if self.board[sq_two] is not None or type(piece) == Pawn:
                    self.fifty_moves = 0

                # setting the en-passent conditions of a pawn when the other pawn is pushed two squares
                if type(piece) == Pawn and not piece.has_moved:
                    if abs(sq_two[1] - sq_one[1]) == 2:
                        try:
                            p_two = self.board[(sq_two[0] + 1, sq_two[1])]
                            if type(p_two) == Pawn and p_two.colour != piece.colour:
                                p_two.can_en_passent = [(sq_two[0], sq_two[1] - 1), self.half_moves]
                        except KeyError:
                            pass
                        try:
                            p_two = self.board[(sq_two[0] - 1, sq_two[1])]
                            if type(p_two) == Pawn and p_two.colour != piece.colour:
                                p_two.can_en_passent = [(sq_two[0], sq_two[1] - 1), self.half_moves]
                        except KeyError:
                            pass

                if self.board[sq_two] is not None:
                    self.remove_piece(sq_two)
                self.board[sq_two] = self.board[sq_one]
                self.board[sq_one] = None
                piece.square = sq_two
                self.half_moves += 1
                self.white_to_move = not self.white_to_move
                piece.has_moved = True if type(piece) in [King, Rook, Pawn] and not piece.has_moved else True
            else:
                raise Exception("That piece cannot move there")

        # moving a black piece
        elif not self.white_to_move and piece.colour == 'black':
            if sq_two in piece.moves:
                self.fifty_moves += 1
                # reset fifty move counter
                if self.board[sq_two] is not None or type(piece) == Pawn:
                    self.fifty_moves = 0

                # setting the en-passent conditions of a pawn when the other pawn is pushed two squares
                if type(piece) == Pawn and not piece.has_moved:
                    piece.has_moved = True
                    if abs(sq_two[1] - sq_one[1]) == 2:
                        try:
                            p_two = self.board[(sq_two[0] + 1, sq_two[1])]
                            if type(p_two) == Pawn and p_two.colour != piece.colour:
                                p_two.can_en_passent = [(sq_two[0], sq_two[1] + 1), self.half_moves]
                        except KeyError:
                            pass
                        try:
                            p_two = self.board[(sq_two[0] - 1, sq_two[1])]
                            if type(p_two) == Pawn and p_two.colour != piece.colour:
                                p_two.can_en_passent = [(sq_two[0], sq_two[1] + 1), self.half_moves]
                        except KeyError:
                            pass

                if self.board[sq_two] is not None:
                    self.remove_piece(sq_two)
                self.board[sq_two] = self.board[sq_one]
                self.board[sq_one] = None
                piece.square = sq_two
                self.half_moves += 1
                self.white_to_move = not self.white_to_move
                piece.has_moved = True if type(piece) in [King, Rook, Pawn] and not piece.has_moved else True
            else:
                raise Exception("That piece cannot move there")
        else:
            raise Exception("Error: Wrong colour piece selected for move.")

        # add the stat to the list of prev states and update the moves for each piece
        self.add_state()
        self.update_moves()
        
        check = self.king_in_check()
        if check is not None:
            check.in_check = True
            print(check.colour + " king is in check!")
        else:
            for piece in self.board.values():
                if type(piece) == King:
                    piece.in_check = False

    def add_state(self):
        b = copy.deepcopy(self.board)
        self.prev_state.append(b)
        self.prev_state.pop(0)
        rep = hash(str(self))
        self.threefold_tracker.append(rep)

    def game_over(self):
        king = self.king_in_check()
        if self.half_moves != 0 and self.threefold_tracker.count(self.threefold_tracker[-1]) == 3:
            self.outcome = 0
            return True
        if king is None:
            return False
        elif king is not None:
            same_colour = []
            for piece in self.board.values():
                if piece is not None and piece.colour == king.colour:
                    same_colour.append(piece)
            for piece in same_colour:
                if len(piece.moves) > 0:
                    return False
            self.outcome = 1 if king.colour == 'white' else -1
            return True

    def board_html(self):
        imgs = {}
        for key, value in self.board.items():
            if value is not None:
                imgs[key] = value.img
        return imgs

    def js_remove(self):
        empty = []
        for key, value in self.board.items():
            if value is None:
                empty.append(str(key))
        return empty

    def update_moves(self, remove=True):
        for piece in self.board.values():
            if piece is not None:
                piece.update_valid_moves(self, remove)

    def remove_piece(self, square):
        piece = self.board[square]
        if piece.colour == 'white':
            self.white_pieces.remove(piece)
        else:
            self.black_pieces.remove(piece)
