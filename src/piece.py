import os

class Piece:
    
    def __init__(self, name, color, value, texture = None, texture_rect = None):        # texture basically means image or image url
        self.name = name
        self.color = color
        value_sign = 1 if color == 'white' else -1              # this statement and the one below makes sense hum value de rhe hai white aur black pieces ko alag, white pieces has +1 * value, black pieces has -1 * value as their value
        self.value = value * value_sign
        self.moves = []                                         # attribute moves | by moves we mean valid moves
        self.moved = False
        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect
        
    def set_texture(self, size = 80):
        self.texture = os.path.join(                            # we need a model that is why used os and imported os above (that's what the video said)
            f'assets/images/imgs-{size}px/{self.color}_{self.name}.png')        # this statement means that first we are accessing assets then images then imgs and then the images with 80 pixels size and then accesing the files with their color_name.png according to how they are stored in file
        
    def add_moves(self, move):
        self.moves.append(move)                                 # append the move to our moves attribute 
        
    def clear_moves(self):
        self.moves = []
    
class Pawn(Piece):                                              # in python in order to tell this class inherits from this class(mother class) we put class which is to be inherited(mother class) in brackets of new class example - class Pawn(Piece)
    
    def __init__(self, color):
        
        
        '''
        In pygame x axis works fine it increases as we go right but in y-axis it increase as we move downwards 
        so in our game we are making it that white pieces are at the bottom and black pieces are at the top so
        if we have a white piece its direction is -1 this means that the white piece should go up because as we
        do -1 the y coordinate increases because in pygame y-axis works reversely\opposite - samjha??
        '''
        
        self.value_sign = 1 if color == 'white' else -1
        self.dir = -1 if color == 'white' else 1                # telling direction to pawn , color white go up (-1 in dir), color black go down (+1 in dir) 
        self.en_passant = False
        super().__init__('pawn', color, 1.0)                    # super() means we are calling the mother class i.e.piece and initializing our values in mother class
        
class Knight(Piece):
    
    def __init__(self, color):                                  # not adding direction here because knights can move anywhere, same with rest chess pieces except pawn which has a fixed direction to move vertically only
        self.value_sign = 1 if color == 'white' else -1
        super().__init__('knight', color, 3.0)                  # the value of these chess pieces defines how important they are if we were to use AI later, these values are true acc. to net
        
class Bishop(Piece):
    
    def __init__(self, color):
        self.value_sign = 1 if color == 'white' else -1
        super().__init__('bishop', color, 3.001)                # bishop and knight have same value but just for sake we use 3.001 here to make bishop slightly more important than our knight

class Rook(Piece):
    
    def __init__(self, color):
        self.value_sign = 1 if color == 'white' else -1
        super().__init__('rook', color, 5.0)
        
class Queen(Piece):
    
    def __init__(self, color):
        self.value_sign = 1 if color == 'white' else -1
        super().__init__('queen', color, 9.0)
        
class King(Piece):
    
    def __init__(self, color):
        self.value_sign = 1 if color == 'white' else -1
        self.left_rook = None
        self.right_rook = None
        super().__init__('king', color, 10000.0)                # king has very high value so that AI can know king is the most important piece