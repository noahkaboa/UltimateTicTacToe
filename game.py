class LittleBoard:
    def __init__(self):
        self.board = [
            ["_"]*3,
            ["_"]*3,
            ["_"]*3
        ]
        self.to_move = "X"

    def __str__(self):
        s = ""
        for row in self.board:
            s += "-".join(row)
            s += "\n"
        return s

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
    
    def make_move(self, row, col, player):
        if self.board[row][col] != "_":
            return False
        self.board[row][col] = player
        self.to_move = "X" if self.to_move == "O" else "O"
        return True

class BigBoard:
    def __init__(self):
        self.big_board = [[LittleBoard()] * 3] * 3
        self.game_state = LittleBoard()
        self.to_move = "X"
        self.prev_move = {
            "small_row": -1,
            "small_col": -1
        }

    def make_move(self, big_row, big_col, small_row, small_col):
        if big_row != self.prev_move["small_row"] or big_col != self.prev_move["small_col"]:
            if self.prev_move["small_row"] != -1:
                return False
            
        if self.big_board[big_row][big_col].make_move(small_row, small_col):
            if self.big_board[big_row][big_col].check_winner():
                self.prev_move["small_row"] = -1
                self.game_state.force_move(big_row, big_col, self.to_move)
            return True
    
    

    

# b = LittleBoard()

# while not b.check_winner():
#     print(b.board)
#     print(f"{b.to_move} to move")

#     valid_move = False
#     while not valid_move:
#         row = int(input("Row:\t"))
#         col = int(input("Col:\t"))
#         valid_move = b.make_move(row, col)
#         if not valid_move:
#             print("Invalid Move! try again")


g = BigBoard()
print(g.game_state)