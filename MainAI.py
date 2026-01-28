# ================================================================
# FILE:			MyAI.py
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
# ================================================================

from AI import AI
from Action import Action


class MyAI( AI ):

    def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
        ########################################################################
        ########################################################################
        self.board = self.create_board(rowDimension, colDimension)
        self.safe_to_uncover = set()
        self.flag_location = set()
        self.rowDimension = rowDimension
        self.colDimension = colDimension
        self.totalMines = totalMines
        self.lastX = startX
        self.lastY = startY
        self.flag = 0
        self.covered = rowDimension * colDimension
        ########################################################################
        ########################################################################


    def getAction(self, number: int) -> "Action Object":

        ########################################################################
        ########################################################################
        
        # print("printing info")
        # print(self.totalMines)
        # print(self.lastX, self.lastY)
        # print("action num", number)
        self.board[self.lastY][self.lastX][1] = number
        # self.print_board()
        if(number == 0):
            self.mark_all_surrounding_safe(self.lastX, self.lastY)
        elif(number == -1):
            # print("decrease bomb surrounding")
            self.board[self.lastY][self.lastX][1] = "F"
            self.update_surrounding_num_bomb(self.lastX, self.lastY)
        else:
            self.update_remaining_covered_all_surrounding(self.lastX, self.lastY)
            
        if(self.safe_to_uncover):
            x, y = self.safe_to_uncover.pop()
            # print(self.safe_to_uncover)
            self.lastX = x
            self.lastY = y
            return Action(AI.Action.UNCOVER, x, y)
        if(self.flag_location):
            x, y = self.flag_location.pop()
            self.lastX = x
            self.lastY = y
            # print("flag x=", x, "y =", y)
            return Action(AI.Action.FLAG, x, y)
# #         # if(self.covered == self.totalMines):
        return Action(AI.Action.LEAVE)
        
        ########################################################################
        #                            MAIN
        ########################################################################

    def print_board(self):
        for i in range(self.rowDimension):
            row_str = " | ".join(str(cell) if cell is not None else " " for cell in self.board[i])
            print(row_str)
            
    def mark_all_surrounding_safe(self, coorX, coorY):
        # print("coorx", coorX, "coorY", coorY)
        startX = coorX - 1 if coorX > 0 else 0
        endX = coorX + 2 if coorX < self.colDimension - 2 else self.colDimension
        startY = coorY - 1 if coorY > 0 else 0
        endY = coorY + 2 if coorY < self.rowDimension - 2 else self.rowDimension
        self.board[coorY][coorX][0] = 0
        for y in range(startY, endY):
            for x in range(startX, endX):
                if(x != coorX or y != coorY):
                    self.board[y][x][0] -= 1
                    if(self.board[y][x][1] is None):
                        self.safe_to_uncover.add((x, y))
                    elif(self.board[y][x][0] != 0 and self.board[y][x][0] == self.board[y][x][1]):
                        # print("LOOKING FOR BOMB")
                        self.find_location_of_bomb(x, y, self.board[y][x][1])
        # self.print_board()
        # print(self.safe_to_uncover)
    
    def update_remaining_covered_all_surrounding(self, coorX, coorY):
        if(self.board[coorY][coorX][0] == self.board[coorY][coorX][1]):
            self.find_location_of_bomb(coorX, coorY, self.board[coorY][coorX][1])
            return
        
        startX = coorX - 1 if coorX > 0 else 0
        endX = coorX + 2 if coorX < self.colDimension - 2 else self.colDimension
        startY = coorY - 1 if coorY > 0 else 0
        endY = coorY + 2 if coorY < self.rowDimension - 2 else self.rowDimension
        
        for y in range(startY, endY):
            for x in range(startX, endX):
                if(x != coorX or y != coorY):
                    self.board[y][x][0] -= 1
                    if(self.board[y][x][0] != 0 and self.board[y][x][0] == self.board[y][x][1]):
                        # print("LOOKING FOR BOMB")
                        self.find_location_of_bomb(x, y, self.board[y][x][1])
        # self.print_board()
        # print("self flag location", self.flag_location)
    
    def update_surrounding_num_bomb(self, coorX, coorY):
        startX = coorX - 1 if coorX > 0 else 0
        endX = coorX + 2 if coorX < self.colDimension - 2 else self.colDimension
        startY = coorY - 1 if coorY > 0 else 0
        endY = coorY + 2 if coorY < self.rowDimension - 2 else self.rowDimension
        mark_safe_positions = set()
        for y in range(startY, endY):
            for x in range(startX, endX):
                if(x != coorX or y != coorY):
                    self.board[y][x][0] -= 1
                    if(self.board[y][x][1] is not None and self.board[y][x][1] != "NF" and self.board[y][x][1] != "F"):
                        self.board[y][x][1] -= 1                  
                    if(self.board[y][x][0] != 0 and self.board[y][x][0] == self.board[y][x][1]):
                        # print("LO/OKING FOR BOMB")
                        self.find_location_of_bomb(x, y, self.board[y][x][1])
                    elif(self.board[y][x][1] == 0):
                        mark_safe_positions.add((x, y))
        # print("BEFORE MARK SAFE POSITION")
        # self.print_board()                
        for x, y in mark_safe_positions:
            # print("y =", y, "x =", x, "tuple", self.board[y][x])
            self.mark_all_surrounding_safe(x, y)
        for tuple_ in self.safe_to_uncover:
            self.flag_location.discard(tuple_)
        # self.print_board()
        # print("self safe_to_uncover", self.safe_to_uncover)
        # print("self flag location", self.flag_location)
    def find_location_of_bomb(self, coorX, coorY, num_of_bomb):
        startX = coorX - 1 if coorX > 0 else 0
        endX = coorX + 2 if coorX < self.colDimension - 2 else self.colDimension
        startY = coorY - 1 if coorY > 0 else 0
        endY = coorY + 2 if coorY < self.rowDimension - 2 else self.rowDimension
        for y in range(startY, endY):
            for x in range(startX, endX):
                if(x != coorX or y != coorY):
                    if(self.board[y][x][1] is None):
                        self.board[y][x][1] = "NF"
                        self.flag_location.add((x, y))
        
    def create_board(self, rowDimension, colDimension):
        board = [[[8, None] for _ in range(colDimension)] for _ in range(rowDimension)]
        for y in [0, rowDimension- 1]:
            for x in [0, colDimension-1]:
                board[y][x][0] = 3
        max_outer_col_index = colDimension - 1
        for x in range(1, max_outer_col_index):
            board[0][x][0] = 5
            board[max_outer_col_index][x][0] = 5
        max_outer_row_index = rowDimension - 1
        for y in range(1, max_outer_row_index):
            board[y][0][0] = 5
            board[y][max_outer_row_index][0] = 5
        return board

