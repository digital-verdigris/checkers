#piece class
class checkers_piece:
    #setup
    def __init__(self, team):
        self._team = team
        self._is_king = False
        self._is_selected = False

    #print to terminal
    def print(self):
        if self._is_king:
            if self._team == 'red':
                name = 'R'
            elif self._team == 'black':
                name = 'B'
            else:
                name = '?'
        else:
            if self._team == 'red':
                name = 'r'
            elif self._team == 'black':
                name = 'b'
            else:
                name = '?'
            
        print(name, end = ' ')
    
    #to set king if needed
    def make_king(self):
        self._is_king = True
    
    def get_king_status(self):
        return self._is_king
    