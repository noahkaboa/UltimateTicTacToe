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
        
    def is_valid_move(self, big_row, big_col, small_row, small_col):
        return self.big_board[big_row][big_col].board[small_row][small_col] == "_" and not self.big_board[big_row][big_col].check_winner() and (self.prev_move["small_row"] == -1 or (big_row == self.prev_move["small_row"] and big_col == self.prev_move["small_col"]))
    
    def board_to_utn(self):
        s = ""
        blank_count = 0
        for big_row in range(3):
            for big_col in range(3):
                for small_row in range(3):
                    for small_col in range(3):
                        if self.big_board[big_row][big_col].board[small_row][small_col] == "_":
                            blank_count += 1
                        else:
                            if blank_count != 0:
                                s += str(blank_count)
                            blank_count = 0
                            s += self.big_board[big_row][big_col].board[small_row][small_col]
        if blank_count != 0:
            s += str(blank_count)

        s += " " + self.to_move
        s += " " + str(self.prev_move["small_row"]) + " " + str(self.prev_move["small_col"])
        return s
    
    def utn_parse(self, s):
        compile = ""
        complete = []
        for letter in s:
            if compile:
                if compile.isdigit() == letter.isdigit():
                    compile += letter
                else:
                    complete.append(compile)
                    compile = letter
            else:
                compile = letter
        if compile:
            complete.append(compile)

        for i in range(len(complete)):
            if complete[i].isalpha():
                if len(complete[i]) > 1:
                    complete[i:i] = [*complete[i]]
                    complete.pop(i+len(complete[i]) + 1)

        full_board = []
        for item in complete:
            if item.isdigit():
                full_board.extend(["_"]*int(item))
            else:
                full_board.append(item)
        
        return full_board

    def utn_to_board(self, s):
        board, player, prev_row, prev_col = s.split(" ")
        items = self.utn_parse(board)
        self.to_move = player
        self.big_board = [[LittleBoard() for _ in range(3)] for _ in range(3)]
        self.game_state = LittleBoard()
        self.prev_move = {
            "small_row": int(prev_row),
            "small_col": int(prev_col)
        }

        item = items.pop(0)

        for big_row_i in range(3):
            for big_col_j in range(3):
                for small_row_k in range(3):
                    for small_col_l in range(3):
                        if items:
                            if isinstance(item, int):
                                if item == 0:
                                    item = items.pop(0)
                                else:
                                    item -= 1
                                    self.big_board[big_row_i][big_col_j].board[small_row_k][small_col_l] = "_"
                            else:
                                self.big_board[big_row_i][big_col_j].board[small_row_k][small_col_l] = item
                                item = items.pop(0)
                                if item.isdigit():
                                    item = int(item)
