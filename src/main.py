
import pygame                                                       # for graphics part
import sys                                                          # for quitting the application

from const import *
from game import Game

from square import Square
from move import Move


class Main:
    
    # init methpd - to initialize
    def __init__(self):                                             # self as parameter
        pygame.init()                                               # whenever using pygame need to initialize | each time we need to create a attribute or keyword hume self keyword se start krna padega
                                              
        self.screen = pygame.display.set_mode( (WIDTH, HEIGHT) )    # Screen attribute | width and height are tuples passed in it | this statement creates a pygame screen and we are saving it on variable self.screen
        pygame.display.set_caption('chess')                         # screen ka caption mtlb screen ka title i.e. chess
        self.game = Game()                                          # making reference from our main class to our game class
        self.value_sign = 0;                                        # this was important to make white & black move one after another, bool krke kr sakte the but aise kr diya
    def mainloop(self):                                             # this is the method preety much responsible of calling all other classes | mainloop is an infinite loop and it is keeping on looping and if we do something on our screen/chess board it updates by the below statement update the next time it loops again
                    
               
        screen = self.screen                                        
        game = self.game                                            # common sense hume baar baar krne ki jarurat nhi padegi
        dragger = self.game.dragger 
        board = self.game.board
        
        while True:
            # show methods
            game.show_bg(screen)                                    # show_bg function mai hum self.screen bhj rhe hai aur woh hume pura background de rha hai according to function show_bg in class Game in file game
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            game.show_hover(screen)
            
            if dragger.dragging:                                    # we did this two statements because without them while moving the piece the the pieces flickers as it dissappears and appears again, this is because if we see the above two statements they both are coinciding and sometimes background bleeds on the piece 
                dragger.update_blit(screen) 
            
            for event in pygame.event.get():                        # we are looping through each event in the screen and if the event is quiting the screen
                
                # dragging processes - 3 processess:-
                # 1st - click - click the piece
                if event.type == pygame.MOUSEBUTTONDOWN:            
                    dragger.update_mouse(event.pos)                 # printing event.pos tells us the postion(x and y coordinate) of our click | we send position of event that is click to update_mouse function in dragger and it stores the position in mouseX and mouseY and gives us position of click
                    
                    clicked_row = dragger.mouseY // SQSIZE          # tells the row number (0 to 7) clicked by mouse
                    clicked_col = dragger.mouseX // SQSIZE          # tells the column number (0 to 7) clicked by mouse
                    
                    # if clicked square has a piece ?
                    if board.squares[clicked_row][clicked_col].has_piece():
                        
                        piece = board.squares[clicked_row][clicked_col].piece
                        if self.value_sign == 0:
                            self.value_sign=piece.value_sign
                            
                            board.calc_moves(piece, clicked_row, clicked_col)
                            dragger.save_initial(event.pos)             # this statement must be in 'IF' cause if it is not in this if statement it will drag empty sqaures and we don't want that | saves the initial position (row and column) of dragger | we need this because in case of an invalid move we want the piece to return to its original position
                            dragger.drag_piece(piece)
                            # show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)
                            self.value_sign = piece.value_sign
                            
                            
                        else:
                            if(piece.value_sign == self.value_sign):
                                board.calc_moves(piece, clicked_row, clicked_col)
                                dragger.save_initial(event.pos)             # this statement must be in 'IF' cause if it is not in this if statement it will drag empty sqaures and we don't want that | saves the initial position (row and column) of dragger | we need this because in case of an invalid move we want the piece to return to its original position
                                dragger.drag_piece(piece)
                                # show methods
                                game.show_bg(screen)
                                game.show_last_move(screen)
                                game.show_moves(screen)
                                game.show_pieces(screen)
                                self.value_sign = piece.value_sign
                                    

                    
                        
                        
                            

                        
                
                # 2nd - mouse motion - moving the piece
                elif event.type == pygame.MOUSEMOTION:     
                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE

                    game.set_hover(motion_row, motion_col)         
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)             # updating the position of the mouse  
                        # show methods            
                        game.show_bg(screen)                        # used this statement because without it we were getting an illusion of multiple same pieces while dragging the pieces, this solves that
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)                    # after solving above bug we get another bug of flickering of every piece of board as background bleeds on pieces hence used this statement
                        game.show_hover(screen)
                        dragger.update_blit(screen)                 # updating the image of the piece to constantly move with the mouse
                        
                 # click release
                elif event.type == pygame.MOUSEBUTTONUP:
                    
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE

                        # create possible move
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        
                        move = Move(initial, final)
                        valid_move = board.valid_move(dragger.piece, move)
                        

                        # print(initial)
                        # print(final)
                        # print(self.value_sign)
                        if initial != final and valid_move:
                            # print('not equal')
                            if self.value_sign == 1:
                                self.value_sign = -1
                                # print(self.value_sign)
                            else:
                                self.value_sign = 1 
                                # print(self.value_sign)
  
                        # valid move ?
                        if board.valid_move(dragger.piece, move):
                            # normal capture
                            captured = board.squares[released_row][released_col].has_piece()

                            board.move(dragger.piece, move)

                            board.set_true_en_passant(dragger.piece)        

                        
                    dragger.undrag_piece()
                    
                
                # quit application
                elif event.type == pygame.QUIT:                       # then the screen quits mtlb ki if X pe click kr rhe hai hum toh screen bnd ho jaane chahiye | pygame.QUIT no brackets
                    pygame.quit()
                    sys.exit()
            
            pygame.display.update()                                 # updating the screen | make sure yeh code for loop ke bahar ho and end mai ho maainloop ke
    
main = Main()                                                       # main jo phle likha hai woh instance bna hai main class ka
main.mainloop() 

'''
ab jab instance bn gya hai humne yeh code kra aur inn dono code
se main class chlte hai starting from __init__ ab yeh nhi pta
ki mainloop pe end hoyegi ya nahi for this ask seniors 
'''