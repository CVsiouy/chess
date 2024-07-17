import pygame

from const import *

class Dragger:
    
    def __init__(self):
        self.piece = None
        self.dragging = False
        self.mouseX = 0
        self.mouseY = 0
        self.initial_row = 0
        self.initial_col = 0
        
    def update_blit(self, surface):
        # texture
        self.piece.set_texture(size = 128)                      # when we are dragging the piece we want the piece to be a little bit bigger while dragging | phle piece ile mai jaata hai wha pe pura execute krta hai using the size= 128 px
        texture = self.piece.texture                            # this is the path to access the file MAYBE | phle piece mai jaata hai wah pe
        img = pygame.image.load(texture)                        # img variable pe uske texture(images) using texture path load ho rhi hai
        # rect                                                  # same thing as we did in game file, show_pieces function - ALMOST
        img_center = (self.mouseX, self.mouseY)                 # our image center should be the position of the mouse that is dragging krte hoye saath mai chle piece
        self.piece.texture_rect = img.get_rect(center = img_center)
        # blit
        surface.blit(img, self.piece.texture_rect)
        
        
    def update_mouse(self, pos):
        self.mouseX, self.mouseY = pos                          # pos:- position :- (x-coordinate, y-coordinate)
        
    def save_initial(self, pos):
        self.initial_row = pos[1] // SQSIZE                     # pos[1] denotes the second element of the pos array or tuple i.e. the y-coordinate | gives maybe initial row of piece MAYBE or the clicked row
        self.initial_col = pos[0] // SQSIZE                     # pos[0] denotes the first element of the pos array or tuple i.e. the x-coordinate | gives maybe initial column of piece MAYBE or the clicked column
        
    def drag_piece(self, piece):
        self.piece = piece
        self.dragging = True
        
    def undrag_piece(self):
        self.piece = None
        self.dragging = False
        