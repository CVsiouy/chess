from const import *
from square import Square
from piece import *
from move import Move
import copy
import os


class Board:
    
    # init method
    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0, ] for col in range(COLS)]      # toh hum sqaures naam se ek list bna rhe hai jismai hum ek pure column ki line mai hr square ki value 0 initialize kr rhe hai(loop ke according hr hr column ki list bn rhi hai jismai hr square ki value 0 ho gyi hai) | here we are badically creating a 2D array
        self.last_move = None
        self._create()                                                          # to assign square object instead of 0 to squares
        self._add_pieces('white')
        self._add_pieces('black')
        
    def move(self, piece, move, testing=False):
        initial = move.initial
        final = move.final

        en_passant_empty = self.squares[final.row][final.col].isempty()

        # console board move update
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        if isinstance(piece, Pawn):
            # en passant capture
            diff = final.col - initial.col
            if diff != 0 and en_passant_empty:
                # console board move update
                self.squares[initial.row][initial.col + diff].piece = None
                self.squares[final.row][final.col].piece = piece
                # if not testing:
                #     sound = Sound(
                #         os.path.join('assets/sounds/capture.wav'))
                #     sound.play()
            
            # pawn promotion
            else:
                self.check_promotion(piece, final)

        # king castling
        if isinstance(piece, King):
            if self.castling(initial, final) and not testing:
                diff = final.col - initial.col
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook, rook.moves[-1])

        # move
        piece.moved = True

        # clear valid moves
        piece.clear_moves()

        # set last move
        self.last_move = move

    def valid_move(self, piece, move):
        return move in piece.moves

    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)

    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2

    def set_true_en_passant(self, piece):
        
        if not isinstance(piece, Pawn):
            return

        for row in range(ROWS):
            for col in range(COLS):
                if isinstance(self.squares[row][col].piece, Pawn):
                    self.squares[row][col].piece.en_passant = False
        
        piece.en_passant = True

    def in_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move, testing=True)
        
        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].has_enemy_piece(piece.color):
                    p = temp_board.squares[row][col].piece
                    temp_board.calc_moves(p, row, col, bool=False)
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            return True
        
        return False
        
    def calc_moves(self, piece, row, col, bool=True):
        '''
        calculate all the possible (valid) moves of an specific piece on a specific position
        '''
        
        def pawn_moves():
            # steps
            steps = 1 if piece.moved else 2

            # vertical moves
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].isempty():
                        # create initial and final move squares
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)
                        # create a new move
                        move = Move(initial, final)

                        # check potencial checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_moves(move)
                        else:
                            # append new move
                            piece.add_moves(move)
                    # blocked
                    else: break
                # not in range
                else: break

            # diagonal moves
            possible_move_row = row + piece.dir
            possible_move_cols = [col-1, col+1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        # create initial and final move squares
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # create a new move
                        move = Move(initial, final)
                        
                        # check potencial checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_moves(move)
                        else:
                            # append new move
                            piece.add_moves(move)

            # en passant moves
            r = 3 if piece.color == 'white' else 4
            fr = 2 if piece.color == 'white' else 5
            # left en pessant
            if Square.in_range(col-1) and row == r:
                if self.squares[row][col-1].has_enemy_piece(piece.color):
                    p = self.squares[row][col-1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            # create initial and final move squares
                            initial = Square(row, col)
                            final = Square(fr, col-1, p)
                            # create a new move
                            move = Move(initial, final)
                            
                            # check potencial checks
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move
                                    piece.add_moves(move)
                            else:
                                # append new move
                                piece.add_moves(move)
            
            # right en pessant
            if Square.in_range(col+1) and row == r:
                if self.squares[row][col+1].has_enemy_piece(piece.color):
                    p = self.squares[row][col+1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            # create initial and final move squares
                            initial = Square(row, col)
                            final = Square(fr, col+1, p)
                            # create a new move
                            move = Move(initial, final)
                            
                            # check potencial checks
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move
                                    piece.add_moves(move)
                            else:
                                # append new move
                                piece.add_moves(move)
        
        def knight_moves():                                                     # can define it outside the calc_moves also, for the sake we just want all moves calculation in calc_moves
            '''
            8 possible moves if knight at center and assuming no other pieces is there
            '''
            possible_moves = [                                                  # variable either an array or list , with 8 tuples to represent moves of knight () - tuple
                (row-2, col+1),                                                 # (up - up - right) row-2 means piece can go up and col+1 means right, so assume a knight at center and go 2 moves up and one piece right that is a move of the knight
                (row-1, col+2),                                                 # (up - right - right) all theses denotes moves of knights
                (row+1, col+2),                                                 # (down - right - right)
                (row+2, col+1),                                                 # (down - down - right)
                (row+2, col-1),                                                 # (down - down - left)
                (row+1, col-2),                                                 # (down - left - left)
                (row-1, col-2),                                                 # (up - left - left)
                (row-2, col-1),                                                 # (up - up - left)
            ]           
            
            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move            # row aur column ka number assign ho rha possible_move mai
                
                if Square.in_range(possible_move_row, possible_move_col):       # if statement executes if all rows and cols are inside the board, common sense thoda dimaag lga
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):        # agar square empty hai ya enemy hai uspe | basically valid moves kr rha yeh
                        # create squares of the new move
                        initial = Square(row, col)                              # initial position of piece
                        final = Square(possible_move_row, possible_move_col)    # piece = piece | position of piece after releasing
                        # create new move
                        move = Move(initial, final)
                        # append new valid move
                        piece.add_moves(move)
                        
                        # check potencial checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_moves(move)
                            else: break
                        else:
                            # append new move
                            piece.add_moves(move)
        
        def straightline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        # create squares of the possible new move
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # create a possible new move
                        move = Move(initial, final)

                        # empty = continue looping
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            # check potencial checks
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move
                                    piece.add_moves(move)
                            else:
                                # append new move
                                piece.add_moves(move)

                        # has enemy piece = add move + break
                        elif self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            # check potencial checks
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move
                                    piece.add_moves(move)
                            else:
                                # append new move
                                piece.add_moves(move)
                            break

                        # has team piece = break
                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break
                    
                    # not in range
                    else: break

                    # incrementing incrs
                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr

        def king_moves():
            adjs = [
                (row-1, col+0), # up
                (row-1, col+1), # up-right
                (row+0, col+1), # right
                (row+1, col+1), # down-right
                (row+1, col+0), # down
                (row+1, col-1), # down-left
                (row+0, col-1), # left
                (row-1, col-1), # up-left
            ]

            # normal moves
            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        # create squares of the new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col) # piece=piece
                        # create new move
                        move = Move(initial, final)
                        # check potencial checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_moves(move)
                            else: break
                        else:
                            # append new move
                            piece.add_moves(move)

            # castling moves
            if not piece.moved:
                # queen castling
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1, 4):
                            # castling is not possible because there are pieces in between ?
                            if self.squares[row][c].has_piece():
                                break

                            if c == 3:
                                # adds left rook to king
                                piece.left_rook = left_rook

                                # rook move
                                initial = Square(row, 0)
                                final = Square(row, 3)
                                moveR = Move(initial, final)

                                # king move
                                initial = Square(row, col)
                                final = Square(row, 2)
                                moveK = Move(initial, final)

                                # check potencial checks
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(left_rook, moveR):
                                        # append new move to rook
                                        left_rook.add_moves(moveR)
                                        # append new move to king
                                        piece.add_moves(moveK)
                                else:
                                    # append new move to rook
                                    left_rook.add_moves(moveR)
                                    # append new move king
                                    piece.add_moves(moveK)

                # king castling
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5, 7):
                            # castling is not possible because there are pieces in between ?
                            if self.squares[row][c].has_piece():
                                break

                            if c == 6:
                                # adds right rook to king
                                piece.right_rook = right_rook

                                # rook move
                                initial = Square(row, 7)
                                final = Square(row, 5)
                                moveR = Move(initial, final)

                                # king move
                                initial = Square(row, col)
                                final = Square(row, 6)
                                moveK = Move(initial, final)

                                # check potencial checks
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(right_rook, moveR):
                                        # append new move to rook
                                        right_rook.add_moves(moveR)
                                        # append new move to king
                                        piece.add_moves(moveK)
                                else:
                                    # append new move to rook
                                    right_rook.add_moves(moveR)
                                    # append new move king
                                    piece.add_moves(moveK)
        
                        
        if isinstance(piece, Pawn):                                             # another way to do this is ' if piece.name == 'pawn': | here we will calculate all moves for any specific pawn piece | if piece is the instance of the pawn class 
            pawn_moves()
        
        elif isinstance(piece, Knight):                                         # if piece is the instance of the Knight class | to code knight its easiest, even easier than pawn 
            knight_moves()
        
        elif isinstance(piece, Bishop):
            straightline_moves([
                (-1, 1), # up-right
                (-1, -1), # up-left
                (1, 1), # down-right
                (1, -1), # down-left
            ])
        
        elif isinstance(piece, Rook):
            straightline_moves([
                (-1, 0), # up
                (0, 1), # right
                (1, 0), # down
                (0, -1), # left
            ])
        
        elif isinstance(piece, Queen):
            straightline_moves([
                (-1, 1), # up-right
                (-1, -1), # up-left
                (1, 1), # down-right
                (1, -1), # down-left
                (-1, 0), # up
                (0, 1), # right
                (1, 0), # down
                (0, -1) # left
            ])
        
        elif isinstance(piece, King):
            king_moves()
        
        
    def _create(self):                                                          # _before the function name denotes that these are private methods
        for row in range(ROWS):                                                 # looping the 2D array and adding sqaure object to respective square
            for col in range(COLS):                                             # accessing each square in board
                self.squares[row][col] = Square(row, col)                       # clicking on Square their are 3 params humne row aur col hi add kre hai 3rd parameter piece hai jisko hum alag se add krenge in def _add_piece | this statement says ki hum hr square ko uske square object se represent krenge, 
                
    def _add_pieces(self, color):
        if color == 'white':
            row_pawn, row_other = (6, 7)                                        # board mai last row humare 7 number pe hai aur second last 6 number pe (8 rows - 0 to 7)
        else:                                                                   # if color white toh 6th row pe pawn aur 7th row pe other pieces 
            row_pawn, row_other = (1, 0)                                        # if color black 1st row pe pawns aur 0th row pe other pieces
        
        '''row_pawn, row_other = (6,7) if color == 'white' else (1, 0)'''       # short way of writing the above if-else statement :)
        
        # pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))    # function _add_pieces ki according common sense hai ki kaise sirf row 0 and 1 pe black pieces aayenge
            
        # knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))        # aur row 6 aur 7 pe sirf white pieces aayenge aur kaise row 1 aur 6 pe hi pawn aayenge sabh common sense
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))
        
        # bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))
        
        # rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))
        
        # queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))        
        # king
        self.squares[row_other][4] = Square(row_other, 4, King(color))
        

         
        