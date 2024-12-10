class LittleBoard:
    def __init__(self):
        self.board = [
            [""]*3,
            [""]*3,
            [""]*3
        ]
        self.status = ""
        self.player_alternator = self.change_players()
        self.to_move = self.player_alternator.__next__()

    def check_rows(self):
        for row in self.board:
            if len(list(set(row))) == 1:
                return row[0]
        return False

    def check_cols(self):
        for i in range(3):
            col = []
            for row in self.board:
                col.append(row[i])
            if len(list(set(col))) == 1:
                return col[0]
        return False
    
    def check_diags(self):
        d1 = [self.board[0][0], self.board[1][1], self.board[2][2]]
        if len(list(set(d1))) == 1:
            return d1[0]
        d2 = [self.board[0][2], self.board[1][1], self.board[2][0]]
        if len(list(set(d2))) == 1:
            return d2[0]
        return False
    
    def check_winner(self):
        r = self.check_rows()
        c = self.check_cols()
        d = self.check_diags()
        if r:
            return r
        if c:
            return c
        if d:
            return d
        return False
    
    def make_move(self, row, col):
        if self.board[row][col] != "":
            return False
        self.board[row][col] = self.to_move
        self.to_move = self.player_alternator.__next__()
        return True
    
    def change_players(self):
        while True:
            yield "X"
            yield "O"
    

b = LittleBoard()

while not b.check_winner():
    print(b.board)
    print(f"{b.to_move} to move")

    valid_move = False
    while not valid_move:
        row = int(input("Row:\t"))
        col = int(input("Col:\t"))
        valid_move = b.make_move(row, col)
        if not valid_move:
            print("Invalid Move! try again")