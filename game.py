import os

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
            if len(list(set(row))) == 1 and not row[0] == "_":
                return row[0]
        return False

    def check_cols(self):
        for i in range(3):
            col = []
            for row in self.board:
                col.append(row[i])
            if len(list(set(col))) == 1 and not col[0] == "_":
                return col[0]
        return False
    
    def check_diags(self):
        d1 = [self.board[0][0], self.board[1][1], self.board[2][2]]
        if len(list(set(d1))) == 1 and not d1[0] == "_":
            return d1[0]
        d2 = [self.board[0][2], self.board[1][1], self.board[2][0]]
        if len(list(set(d2))) == 1 and not d2[0] == "_":
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
        self.big_board = [[LittleBoard() for _ in range(3)] for _ in range(3)]
        self.game_state = LittleBoard()
        self.to_move = "X"
        self.prev_move = {
            "small_row": -1,
            "small_col": -1
        }

    def __str__(self):
        rows = []
        for big_row in range(3):
            little_rows = [""] * 3
            for big_col in range(3):
                little_board = self.big_board[big_row][big_col]
                for i in range(3):
                    little_rows[i] += " ".join(little_board.board[i]) + "\t"
            rows.extend(little_rows)
            rows.append("")

        return "\n".join(rows)

    def make_move(self, big_row, big_col, small_row, small_col):
        if big_row != self.prev_move["small_row"] or big_col != self.prev_move["small_col"]:
            if self.prev_move["small_row"] != -1:
                return False
        if self.big_board[big_row][big_col].check_winner():
            return False
        
            
        if self.big_board[big_row][big_col].make_move(small_row, small_col, self.to_move):
            self.prev_move["small_row"] = small_row
            self.prev_move["small_col"] = small_col
            
            if self.big_board[big_row][big_col].check_winner():
                self.game_state.make_move(big_row, big_col, self.to_move)

            if self.big_board[small_row][small_col].check_winner():
                self.prev_move["small_row"] = -1

            self.to_move = "X" if self.to_move == "O" else "O"
            
            return True
        else:
            return False
        

    

    

# b = LittleBoard()

# while not b.check_winner():
#     print(b.board)
#     print(f"{b.to_move} to move")

#     valid_move = False
#     while not valid_move:
#         row = int(input("Row:\t"))
#         col = int(input("Col:\t"))
#         valid_move = b.make_move(row, col, b.to_move)
#         if not valid_move:
#             print("Invalid Move! try again")


class Game:
    def __init__(self):
        self.board = BigBoard()

    def play(self):
        while not self.board.game_state.check_winner() in ["X", "O"]:
            print(self.board.game_state)
            print(self.board)
            print(f"{self.board.to_move} to move")
            print(f"{self.board.prev_move=}")

            
            valid_move = False
            while not valid_move:
                big_row = input("Big Row:\t")
                if big_row.isdigit():
                    big_row = int(big_row)
                else:
                    print("Invalid Move! Try again")
                    continue
                big_col = input("Big Col:\t")
                if big_col.isdigit():
                    big_col = int(big_col)
                else:
                    print("Invalid Move! Try again")
                    continue
                small_row = input("Small Row:\t")
                if small_row.isdigit():
                    small_row = int(small_row)
                else:
                    print("Invalid Move! Try again")
                    continue
                small_col = input("Small Col:\t")
                if small_col.isdigit():
                    small_col = int(small_col)
                else:
                    print("Invalid Move! Try again")
                    continue
                
                valid_move = self.board.make_move(big_row, big_col, small_row, small_col)
                if not valid_move:
                    print("Invalid Move! Try again")
    