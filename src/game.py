import pygame

from const import *
from board import Board
from dragger import Dragger
from square import Square 


class Game:                                                                 # game class responsible of all rendering methods | Rendering - process of generating - image by means of a computer program
    
    def __init__(self):
        self.next_player = 'white'
        self.hovered_sqr = None
        self.board = Board()
        self.dragger = Dragger()
    
    # show methods
    
    def show_bg(self, surface):                                             # show background | parameter surface is the screen which we will recieve
        for row in range(ROWS):
            for col in range(COLS):                                         # in here we will draw pattern of chess board(background)
                if (row + col ) % 2 == 0:                                   # common sense ki kaise pattern bna
                    color = (234, 235, 200) # light green
                else:                                                       # rect function has 4 parameters | first parameter is where we are going to start on x-axis
                    color = (119, 154, 88) # dark green                     # second parameter is where we are going to start on y-axis     
                                                                            
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)         # last two params(short of parameters) are going to be width and height                    
                pygame.draw.rect(surface, color, rect)                      # Pygame uses Rect objects to store and manipulate rectangular areas
                                    
                                                                            # ek rectangle ka size chess board ke ek square jitna hoga aur ab yeh
                                                                            # rectangle draw hoga (pygame.draw statement se) screen pe, with associated
                                                                            # color and with associated dimensions according to rect
                 
                '''                   
                # row coordinates
                if col == 0:
                    # color
                    if (row + col ) % 2 == 0:
                        color = (234, 235, 200) # light green
                    else:
                        color = (119, 154, 88) # dark green
                    # label
                    lbl = self.config.font.render(str(ROWS-row), 1, color)
                    lbl_pos = (5, 5 + row * SQSIZE)
                    # blit
                    surface.blit(lbl, lbl_pos)

                # col coordinates
                if row == 7:
                    # color
                    if (row + col ) % 2 == 0:
                        color = (234, 235, 200) # light green
                    else:
                        color = (119, 154, 88) # dark green
                    # label
                    lbl = self.config.font.render(Square.get_alphacol(col), 1, color)
                    lbl_pos = (col * SQSIZE + SQSIZE - 20, HEIGHT - 20)
                    # blit
                    surface.blit(lbl, lbl_pos)
            '''

    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                # piece ?
                if self.board.squares[row][col].has_piece():                # checking if a square has a piece
                    piece = self.board.squares[row][col].piece              # if there is a piece on the square, we are saving that piece on the variable piece
                    
                    # all pieces except dragger piece
                    if piece is not self.dragger.piece:                     # used this if statement as without it when we used to drag a piece the piece size increases to 128 pixels and moves with the mouse but also the same piece size increase to 128 pixels and stays in the initial position so used this statement to make the piece at initial position dissappear | baaki samjh nhi aaya kaise work kra dekh liyo                 
                        piece.set_texture(size = 80)                        # used this statement because without it when we dragged a piece and made an invalid move the piece returns to it's initial location but with 128 pixels size, we want the piece to be 80 pixels while on board so used this
                        img = pygame.image.load(piece.texture)                                      # we are loading the texture(image) of the piece and then saving the image on the variable img
                        img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2         # creating a variable and giving it the position of the center of the square
                        piece.texture_rect = img.get_rect(center = img_center)                      # get_rect is a pygame method (because our img is a pygame image) to get the rectangle area of the surface\screen | here we are centering the img
                        surface.blit(img, piece.texture_rect)                                       # blit basically means put, here we will be putting the chess pieces on the squares , two params 1st img tells the image to blit and 2nd parameter piece.texture_rect tells the position of the img to be blit | surface.blit tells to blit on the surface
    
    def show_moves(self, surface):                                          # we wanna show the moves of the piece that is being dragged 
        if self.dragger.dragging:
            piece = self.dragger.piece                                      # piece we are dragging
            
            # loop all valid moves
            for move in piece.moves:                                                                # similar to above in show_background
                # color
                color = '#C86464' if (move.final.row + move.final.col) % 2 == 0 else '#C84646'      # if color is light red, else color is dark red | yeh waala code smjha nahi mtlb red ho jaana chahiye square pr executing ke time pura time bss red color hi hota hai no light nor dark
                # rect
                rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)
                
    def show_last_move(self, surface):
        # theme = self.config.theme

        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                # # color
                # color = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark
                # rect
                rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
                # blit
                # pygame.draw.rect(surface, color, rect)

                color = (121, 123, 200) # kuch toh color hai randomly choose kra maine

                pygame.draw.rect(surface, color, rect)
                
    def show_hover(self, surface):
        if self.hovered_sqr:
            # color
            color = (180, 180, 180)
            # rect
            rect = (self.hovered_sqr.col * SQSIZE, self.hovered_sqr.row * SQSIZE, SQSIZE, SQSIZE)
            # blit
            pygame.draw.rect(surface, color, rect, width=3)

    # other methods

    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'

    def set_hover(self, row, col):
        self.hovered_sqr = self.board.squares[row][col]

    # def change_theme(self):
    #     self.config.change_theme()

    # def play_sound(self, captured=False):
    #     if captured:
    #         self.config.capture_sound.play()
    #     else:
    #         self.config.move_sound.play()

    def reset(self):
        self.__init__()
                