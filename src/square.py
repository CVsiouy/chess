'''
class Square:
    
    def __init__(self, row, col, piece = None):                         # hume initialize mai params mai self aur square ka row aur col toh milega hi position ke liye, aur piece bhi ek parameter hoga with default value none to represent whether that square has a piece on it or not
        
        self.row = row
        self.col = col
        self.piece = piece
        
    def has_piece(self):
        return self.piece != None                                       # pta nahi kya hai 1 hour time pe kra hai yeh video mai dekh liyo mn nhi hai | basic definition toh yeh lg rhi hai ki check kr rha hai ki piece hai ya nahi baaki kaise - senior
    
    def isempty(self):
        return not self.has_piece()                                     # return if do not have a piece as denoted by not then has.piece function
    
    def has_team_piece(self, color):                                    
        return self.has_piece() and self.piece.color == color           # return if the there is a piece whose color is same to our piece team i.e. to check allied piece 
    
    def has_enemy_piece(self, color):
        return self.has_piece() and self.piece.color != color           # return if there is a piece whose color is opposite to our piece team i.e. to check enemy piece 
    
    def isempty_or_enemy(self, color):
        return self.isempty() or self.has_enemy_piece(color)            # common sense ab toh ki return krega if empty or rival piece
    
    
    /* THIS PART IS COMMENT
    static method is a method in which we can call a method such as function in_range
    with the class without the need of the object or the instance of that class
    for example :-
    s = Square() - this is the instance of the class Square 
        now if static method is not there we need to call  
    s.in_range everytime
    with static method 
    you can simply print without an object or instance of the class - example - 
    Square.in_range(8, 2, 5, 7) --- acc. to below code it will return false because 8 is outside the board i.e. 0 to 7
    Square.in_range(5, 2, 5, 7, 6, 0) --- True   ,,, any number of params
    
    @ - called decorators - do some research about it
    
    after using static method we cannnot call initially like in the 1st example that will not be possible maybe
    
    */
    
    
    @staticmethod               
    def in_range(*args):                                                # *args tells the compiler or whatever that the function can recieve as many parameters as we want | basically a list of arguments | the function is telling us if all arguments are inside the board or not
        for arg in args:                                                # looping our parameter
            if arg < 0 or arg > 7:                  
                return False
            
        return True
    
'''

class Square:

    ALPHACOLS = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}

    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece
        self.alphacol = self.ALPHACOLS[col]

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def has_piece(self):
        return self.piece != None

    def isempty(self):
        return not self.has_piece()

    def has_team_piece(self, color):
        return self.has_piece() and self.piece.color == color

    def has_enemy_piece(self, color):
        return self.has_piece() and self.piece.color != color

    def isempty_or_enemy(self, color):
        return self.isempty() or self.has_enemy_piece(color)

    @staticmethod
    def in_range(*args):
        for arg in args:
            if arg < 0 or arg > 7:
                return False
        
        return True

    @staticmethod
    def get_alphacol(col):
        ALPHACOLS = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
        return ALPHACOLS[col]
    
    