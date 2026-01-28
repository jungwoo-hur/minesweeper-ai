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
import copy

class MyAI(AI):

    class Cell:
        def __init__(self):
            self.mine = False
            self.open = False
            self.neighbors = 0
            self.flag = False
            self.edge = False
            self.edgeCount = 0
            self.mineArr = []  # 이 부분은 용도에 따라 배열로 사용할 수 있습니다.
            self.probability = -1

        def __str__(self):
            # Returns a string representation of the Cell's current state using .format() for Python 3.5 compatibility
            return ("Mine: {}, Open: {}, Neighbors: {}, Flag: {}, Edge: {}, EdgeCount: {}, MineArr: {}, Probability: {}"
                    .format(self.mine, self.open, self.neighbors, self.flag, self.edge, self.edgeCount, self.mineArr, self.probability))


    def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
        ########################################################################
        ########################################################################
        
        # Initialize the game parameters
        self.rowDimension = rowDimension
        self.colDimension = colDimension
        self.totalMines = totalMines

        # Set the starting tile as uncovered
        self.lastX = startX
        self.lastY = startY
        
        self.hundredCount = 0
        self.numberofMines = totalMines

         # Initialize the mine grid with Cell instances
        self.mineGrid = [[self.Cell() for _ in range(rowDimension)] for _ in range(colDimension)]

        self.arrGrid = []
        self.edgeArr = []

        self.mineGrid[startX][startY].open = True

        self.allProbability = True
       


        ########################################################################
        ########################################################################

#################################################################################################### 
        
    def edgeCount(self):
        numRows = self.rowDimension
        numColumns = self.colDimension
        for i in range(numRows):
            for j in range(numColumns):
                count = 0
                if self.mineGrid[i][j].open:
                    self.mineGrid[i][j].edge = False
                    # Left
                    if j > 0 and not self.mineGrid[i][j-1].open:
                        self.mineGrid[i][j-1].edge = True
                        count += 1
                    # Upper Left
                    if i > 0 and j > 0 and not self.mineGrid[i-1][j-1].open:
                        self.mineGrid[i-1][j-1].edge = True
                        count += 1
                    # Up
                    if i > 0 and not self.mineGrid[i-1][j].open:
                        self.mineGrid[i-1][j].edge = True
                        count += 1
                    # Upper Right
                    if i > 0 and j < numColumns - 1 and not self.mineGrid[i-1][j+1].open:
                        self.mineGrid[i-1][j+1].edge = True
                        count += 1
                    # Right
                    if j < numColumns - 1 and not self.mineGrid[i][j+1].open:
                        self.mineGrid[i][j+1].edge = True
                        count += 1
                    # Bottom Right
                    if i < numRows - 1 and j < numColumns - 1 and not self.mineGrid[i+1][j+1].open:
                        self.mineGrid[i+1][j+1].edge = True
                        count += 1
                    # Bottom
                    if i < numRows - 1 and not self.mineGrid[i+1][j].open:
                        self.mineGrid[i+1][j].edge = True
                        count += 1
                    # Bottom Left
                    if i < numRows - 1 and j > 0 and not self.mineGrid[i+1][j-1].open:
                        self.mineGrid[i+1][j-1].edge = True
                        count += 1
                self.mineGrid[i][j].edgeCount = count

        # print("Edge Counts for each cell:")
        # for i in range(self.rowDimension):
        #     for j in range(self.colDimension):
        #         print("Cell ({}, {}): {}".format(i + 1, j + 1, self.mineGrid[i][j].edgeCount), end=' ')
        #     print()  # 줄바꿈을 추가하여 각 행을 구분합니다.


####################################################################################################     


####################################################################################################     
                
    def probability_zero_count(self, i, j):
        count = 0
        # Left
        if j > 0:
            if self.mineGrid[i][j-1].probability == 0:
                count += 1
        # Upper Left
        if i > 0 and j > 0:
            if self.mineGrid[i-1][j-1].probability == 0:
                count += 1
        # Up
        if i > 0:
            if self.mineGrid[i-1][j].probability == 0:
                count += 1
        # Upper Right
        if i > 0 and j < self.colDimension - 1:
            if self.mineGrid[i-1][j+1].probability == 0:
                count += 1
        # Right
        if j < self.colDimension - 1:
            if self.mineGrid[i][j+1].probability == 0:
                count += 1
        # Bottom Right
        if i < self.rowDimension - 1 and j < self.colDimension - 1:
            if self.mineGrid[i+1][j+1].probability == 0:
                count += 1
        # Bottom
        if i < self.rowDimension - 1:
            if self.mineGrid[i+1][j].probability == 0:
                count += 1
        # Bottom Left
        if i < self.rowDimension - 1 and j > 0:
            if self.mineGrid[i+1][j-1].probability == 0:
                count += 1

        return count


####################################################################################################

    def rule_one(self):
        ret = False
        numRows = self.rowDimension
        numColumns = self.colDimension

        # count = 0

        for i in range(numRows):
            for j in range(numColumns):
                
                if (self.mineGrid[i][j].edgeCount > 0 and
                        self.mineGrid[i][j].neighbors == self.mineGrid[i][j].edgeCount - self.probability_zero_count(i, j)):
                    
                    # count += 1
                    # print("check rule_one {}".format(count))

                    # Left
                    if j > 0 :
                        if self.mineGrid[i][j-1].edge and self.mineGrid[i][j-1].probability < 0:
                            self.mineGrid[i][j-1].probability = 100
                            self.hundredCount += 1
                            ret = True
                            
                    # Upper Left
                    if i > 0 and j > 0:
                        if self.mineGrid[i-1][j-1].edge and self.mineGrid[i-1][j-1].probability < 0:
                            self.mineGrid[i-1][j-1].probability = 100
                            self.hundredCount += 1
                            ret = True
                    # Up
                    if i > 0:
                        if self.mineGrid[i-1][j].edge and self.mineGrid[i-1][j].probability < 0:
                            self.mineGrid[i-1][j].probability = 100
                            self.hundredCount += 1
                            ret = True
                    # Upper Right
                    if i > 0 and j < numColumns - 1:
                        if self.mineGrid[i-1][j+1].edge and self.mineGrid[i-1][j+1].probability < 0:
                            self.mineGrid[i-1][j+1].probability = 100
                            self.hundredCount += 1
                            ret = True
                    # Right
                    if j < numColumns - 1:
                        if self.mineGrid[i][j+1].edge and self.mineGrid[i][j+1].probability < 0:
                            self.mineGrid[i][j+1].probability = 100
                            self.hundredCount += 1
                            ret = True
                    # Bottom Right
                    if i < numRows - 1 and j < numColumns - 1:
                        if self.mineGrid[i+1][j+1].edge and self.mineGrid[i+1][j+1].probability < 0:
                            self.mineGrid[i+1][j+1].probability = 100
                            self.hundredCount += 1
                            ret = True
                    # Bottom
                    if i < numRows - 1:
                        if self.mineGrid[i+1][j].edge and self.mineGrid[i+1][j].probability < 0:
                            self.mineGrid[i+1][j].probability = 100
                            self.hundredCount += 1
                            ret = True
                    # Bottom Left
                    if i < numRows - 1 and j > 0:
                        if self.mineGrid[i+1][j-1].edge and self.mineGrid[i+1][j-1].probability < 0:
                            self.mineGrid[i+1][j-1].probability = 100
                            self.hundredCount += 1
                            ret = True
        return ret

   
####################################################################################################     
    
    def probability_hundred_count(self, i, j):
        count = 0
        # Left
        if j > 0:
            if self.mineGrid[i][j-1].probability == 100:
                count += 1
        # Upper Left
        if i > 0 and j > 0:
            if self.mineGrid[i-1][j-1].probability == 100:
                count += 1
        # Up
        if i > 0:
            if self.mineGrid[i-1][j].probability == 100:
                count += 1
        # Upper Right
        if i > 0 and j < self.colDimension - 1:
            if self.mineGrid[i-1][j+1].probability == 100:
                count += 1
        # Right
        if j < self.colDimension - 1:
            if self.mineGrid[i][j+1].probability == 100:
                count += 1
        # Bottom Right
        if i < self.rowDimension - 1 and j < self.colDimension - 1:
            if self.mineGrid[i+1][j+1].probability == 100:
                count += 1
        # Bottom
        if i < self.rowDimension - 1:
            if self.mineGrid[i+1][j].probability == 100:
                count += 1
        # Bottom Left
        if i < self.rowDimension - 1 and j > 0:
            if self.mineGrid[i+1][j-1].probability == 100:
                count += 1

        return count

#################################################################################################### 

    def rule_two(self):
        # count = 0
        ret = False
        numRows = self.rowDimension
        numColumns = self.colDimension
        for i in range(numRows):
            for j in range(numColumns):
                
                if (self.mineGrid[i][j].edgeCount > 0 and
                        self.mineGrid[i][j].neighbors == self.probability_hundred_count(i, j)):
                    
                    # count += 1
                    # print("check rule_two {}".format(count))

                    # Left
                    if j > 0:
                        if self.mineGrid[i][j-1].edge and self.mineGrid[i][j-1].probability < 0:
                            self.mineGrid[i][j-1].probability = 0
                            ret = True
                    # Upper Left
                    if i > 0 and j > 0:
                        if self.mineGrid[i-1][j-1].edge and self.mineGrid[i-1][j-1].probability < 0:
                            self.mineGrid[i-1][j-1].probability = 0
                            ret = True
                    # Up
                    if i > 0:
                        if self.mineGrid[i-1][j].edge and self.mineGrid[i-1][j].probability < 0:
                            self.mineGrid[i-1][j].probability = 0
                            ret = True
                    # Upper Right
                    if i > 0 and j < numColumns - 1:
                        if self.mineGrid[i-1][j+1].edge and self.mineGrid[i-1][j+1].probability < 0:
                            self.mineGrid[i-1][j+1].probability = 0
                            ret = True
                    # Right
                    if j < numColumns - 1:
                        if self.mineGrid[i][j+1].edge and self.mineGrid[i][j+1].probability < 0:
                            self.mineGrid[i][j+1].probability = 0
                            ret = True
                    # Bottom Right
                    if i < numRows - 1 and j < numColumns - 1:
                        if self.mineGrid[i+1][j+1].edge and self.mineGrid[i+1][j+1].probability < 0:
                            self.mineGrid[i+1][j+1].probability = 0
                            ret = True
                    # Bottom
                    if i < numRows - 1:
                        if self.mineGrid[i+1][j].edge and self.mineGrid[i+1][j].probability < 0:
                            self.mineGrid[i+1][j].probability = 0
                            ret = True
                    # Bottom Left
                    if i < numRows - 1 and j > 0:
                        if self.mineGrid[i+1][j-1].edge and self.mineGrid[i+1][j-1].probability < 0:
                            self.mineGrid[i+1][j-1].probability = 0
                            ret = True
        return ret

#################################################################################################### 
    
    # Count how many cells that are open are around a cell
    def open_count(self, i, j): #디버깅
        count = 0
                

        # Left
        if j > 0:
            if self.mineGrid[i][j-1].open == True:
                #print("openCount = {}".format(self.mineGrid[i][j-1].open))
                count += 1
        # Upper Left
        if i > 0 and j > 0:
            if self.mineGrid[i-1][j-1].open:
                #print("openCount = {}".format(self.mineGrid[i-1][j-1].open))
                count += 1
        # Up
        if i > 0:
            if self.mineGrid[i-1][j].open:
                #print("openCount = {}".format(self.mineGrid[i-1][j].open))
                count += 1
        # Upper Right
        if i > 0 and j < (self.colDimension - 1):
            if self.mineGrid[i-1][j+1].open:
                #print("openCount = {}".format(self.mineGrid[i-1][j+1].open))
                count += 1
        # Right
        if j < (self.colDimension - 1):
            if self.mineGrid[i][j+1].open:
                #print("openCount = {}".format(self.mineGrid[i][j+1].open))
                count += 1
        # Bottom Right
        if i < (self.rowDimension - 1) and j < (self.colDimension - 1):
            if self.mineGrid[i+1][j+1].open:
                #print("openCount = {}".format(self.mineGrid[i+1][j+1].open))
                count += 1
        # Bottom
        if i < (self.rowDimension - 1):
            if self.mineGrid[i+1][j].open:
                #print("openCount = {}".format(self.mineGrid[i+1][j].open))
                count += 1
        # Bottom Left
        if i < (self.rowDimension - 1) and j > 0:
            if self.mineGrid[i+1][j-1].open:
                #print("openCount = {}".format(self.mineGrid[i+1][j-1].open))
                count += 1
        return count


####################################################################################################

    def rule_three(self):
        num_rows = self.rowDimension
        num_columns = self.colDimension
        for i in range(num_rows):
            for j in range(num_columns):
                if self.mineGrid[i][j].edgeCount > 2:
                    
                    # 디버깅
                    # print("check sell ({}, {})".format(i + 1, j + 1))
                    
                    # print("Edge Counts for each cell:")
                    # for i in range(self.rowDimension):
                    #     for j in range(self.colDimension):
                    #         print("Cell ({}, {}): {}".format(i + 1, j + 1, self.mineGrid[i][j].edgeCount), end=' ')
                    #     print()  


                    count = 0
                    # Left
                    if j > 0:
                        if self.mineGrid[i][j-1].edge and self.open_count(i, j-1) == 1:
                            count += 1
                    # Upper Left
                    if i > 0 and j > 0:
                        if self.mineGrid[i-1][j-1].edge and self.open_count(i-1, j-1) == 1:
                            count += 1
                    # Up
                    if i > 0:
                        if self.mineGrid[i-1][j].edge and self.open_count(i-1, j) == 1:
                            count += 1
                    # Upper Right
                    if i > 0 and j < (num_columns-1):
                        if self.mineGrid[i-1][j+1].edge and self.open_count(i-1, j+1) == 1:
                            count += 1
                    # Right
                    if j < (num_columns-1):
                        if self.mineGrid[i][j+1].edge and self.open_count(i, j+1) == 1:
                            count += 1
                    # Bottom Right
                    if i < (num_rows-1) and j < (num_columns-1):
                        if self.mineGrid[i+1][j+1].edge and self.open_count(i+1, j+1) == 1:
                            count += 1
                    # Bottom
                    if i < (num_rows-1):
                        if self.mineGrid[i+1][j].edge and self.open_count(i+1, j) == 1:
                            count += 1
                    # Bottom Left
                    if i < (num_rows-1) and j > 0:
                        if self.mineGrid[i+1][j-1].edge and self.open_count(i+1, j-1) == 1:
                            count += 1
                    if count == self.mineGrid[i][j].edgeCount:
                        # print("how many openCount = {}".format(count))
                        # print("anything enter?")

                        probability = round(self.mineGrid[i][j].neighbors / self.mineGrid[i][j].edgeCount * 100)

                        # print("calculated probability = {}".format(probability))
                        # Set probability for each direction
                        # left
                        if j > 0:
                            self.mineGrid[i][j-1].probability = probability
                        # Upper left
                        if i > 0 and j > 0:
                            self.mineGrid[i-1][j-1].probability = probability
                        # Up
                        if i > 0:
                            self.mineGrid[i-1][j].probability = probability
                        # Upper right
                        if i > 0 and j < (num_columns-1):
                            self.mineGrid[i-1][j+1].probability = probability
                        # Right
                        if j < (num_columns-1):
                            self.mineGrid[i][j+1].probability = probability
                        # Bottom right
                        if i < (num_rows-1) and j < (num_columns-1):
                            self.mineGrid[i+1][j+1].probability = probability
                        # Bottom
                        if i < (num_rows-1):
                            self.mineGrid[i+1][j].probability = probability
                        # Bottom left
                        if i < (num_rows-1) and j > 0:
                            self.mineGrid[i+1][j-1].probability = probability

####################################################################################################
                
    def find_next_edge(self, x, y):
        # Iterate over the grid starting from position (x, y)
        num_rows = self.rowDimension
        num_columns = self.colDimension

        for i in range(x, num_rows):
            for j in range(y, num_columns):
                # Check if the cell is an edge and its probability is not assigned
                if self.mineGrid[i][j].edge and self.mineGrid[i][j].probability < 0:
                    return i, j
            # Reset y to 0 after the first iteration
            y = 0
        return -1, -1


####################################################################################################
    
    # Count how many theoretical mines are placed around a cell when generating arrangements  
    def mine_count(self, arrGrid, i, j):
        count = 0
        for k in range(len(arrGrid)):
            if arrGrid[k]['r'] >= i - 1 and arrGrid[k]['r'] <= i + 1 and arrGrid[k]['c'] >= j - 1 and arrGrid[k]['c'] <= j + 1:
                if self.grid[k].mine == True:
                    count += 1
        return count

####################################################################################################


    def can_be_mine(self, i, j):
        # Left
        if j > 0:
            if self.mineGrid[i][j-1].open and self.mineGrid[i][j-1].neighbors <= self.mine_count(self.arrGrid, i, j-1) + self.probability_hundred_count(i, j-1):
                return False
        # Upper Left
        if i > 0 and j > 0:
            if self.mineGrid[i-1][j-1].open and self.mineGrid[i-1][j-1].neighbors <= self.mine_count(self.arrGrid, i-1, j-1) + self.probability_hundred_count(i-1, j-1):
                return False
        # Up
        if i > 0:
            if self.mineGrid[i-1][j].open and self.mineGrid[i-1][j].neighbors <= self.mine_count(self.arrGrid, i-1, j) + self.probability_hundred_count(i-1, j):
                return False
        # Upper Right
        if i > 0 and j < self.colDimension - 1:
            if self.mineGrid[i-1][j+1].open and self.mineGrid[i-1][j+1].neighbors <= self.mine_count(self.arrGrid, i-1, j+1) + self.probability_hundred_count(i-1, j+1):
                return False
        # Right
        if j < self.colDimension - 1:
            if self.mineGrid[i][j+1].open and self.mineGrid[i][j+1].neighbors <= self.mine_count(self.arrGrid, i, j+1) + self.probability_hundred_count(i, j+1):
                return False
        # Bottom Right
        if i < self.rowDimension - 1 and j < self.colDimension - 1:
            if self.mineGrid[i+1][j+1].open and self.mineGrid[i+1][j+1].neighbors <= self.mine_count(self.arrGrid, i+1, j+1) + self.probability_hundred_count(i+1, j+1):
                return False
        # Bottom
        if i < self.rowDimension - 1:
            if self.mineGrid[i+1][j].open and self.mineGrid[i+1][j].neighbors <= self.mine_count(self.arrGrid, i+1, j) + self.probability_hundred_count(i+1, j):
                return False
        # Bottom Left
        if i < self.rowDimension - 1 and j > 0:
            if self.mineGrid[i+1][j-1].open and self.mineGrid[i+1][j-1].neighbors <= self.mine_count(self.arrGrid, i+1, j-1) + self.probability_hundred_count(i+1, j-1):
                return False

        return True


####################################################################################################
    
    def no_mine_count(self, i, j):
        count = 0
        for k in range(len(self.arrGrid)):
            if self.arrGrid[k]['r'] >= i - 1 and self.arrGrid[k]['r'] <= i + 1 and self.arrGrid[k]['c'] >= j - 1 and self.arrGrid[k]['c'] <= j + 1:
                if not self.arrGrid[k].mine:
                    count += 1
        return count

####################################################################################################    

    def can_not_be_mine(self, i, j):
        # Left
        if j > 0:
            if self.mineGrid[i][j-1].open and self.mineGrid[i][j-1].neighbors >= self.mineGrid[i][j-1].edgeCount - self.no_mine_count(i, j-1) - self.probability_zero_count(i, j-1):
                return False
        # Upper Left
        if i > 0 and j > 0:
            if self.mineGrid[i-1][j-1].open and self.mineGrid[i-1][j-1].neighbors >= self.mineGrid[i-1][j-1].edgeCount - self.no_mine_count(i-1, j-1) - self.probability_zero_count(i-1, j-1):
                return False
        # Up
        if i > 0:
            if self.mineGrid[i-1][j].open and self.mineGrid[i-1][j].neighbors >= self.mineGrid[i-1][j].edgeCount - self.no_mine_count(i-1, j) - self.probability_zero_count(i-1, j):
                return False
        # Upper Right
        if i > 0 and j < self.colDimension - 1:
            if self.mineGrid[i-1][j+1].open and self.mineGrid[i-1][j+1].neighbors >= self.mineGrid[i-1][j+1].edgeCount - self.no_mine_count(i-1, j+1) - self.probability_zero_count(i-1, j+1):
                return False
        # Right
        if j < self.colDimension - 1:
            if self.mineGrid[i][j+1].open and self.mineGrid[i][j+1].neighbors >= self.mineGrid[i][j+1].edgeCount - self.no_mine_count(i, j+1) - self.probability_zero_count(i, j+1):
                return False
        # Bottom Right
        if i < self.rowDimension - 1 and j < self.colDimension - 1:
            if self.mineGrid[i+1][j+1].open and self.mineGrid[i+1][j+1].neighbors >= self.mineGrid[i+1][j+1].edgeCount - self.no_mine_count(i+1, j+1) - self.probability_zero_count(i+1, j+1):
                return False
        # Bottom
        if i < self.rowDimension - 1:
            if self.mineGrid[i+1][j].open and self.mineGrid[i+1][j].neighbors >= self.mineGrid[i+1][j].edgeCount - self.no_mine_count(i+1, j) - self.probability_zero_count(i+1, j):
                return False
        # Bottom Left
        if i < self.rowDimension - 1 and j > 0:
            if self.mineGrid[i+1][j-1].open and self.mineGrid[i+1][j-1].neighbors >= self.mineGrid[i+1][j-1].edgeCount - self.no_mine_count(i+1, j-1) - self.probability_zero_count(i+1, j-1):
                return False

        return True

####################################################################################################
    
    def generate_arrangements(self, grid, index): #체크 요망

        i = grid[index]['r']
        j = grid[index]['c']
        if self.can_be_mine(grid, i, j):  # can_be_mine과 can_not_be_mine도 grid를 받도록 수정 필요
            pattern_yes = copy.deepcopy(grid)
            pattern_yes[index].mine = True
            if index < len(grid) - 1:
                self.generate_arrangements(pattern_yes, index + 1)
            else:
                self.edgeArr.append(pattern_yes)

        if self.can_not_be_mine(grid, i, j):
            pattern_no = copy.deepcopy(grid)
            pattern_no[index].mine = False
            if index < len(grid) - 1:
                self.generate_arrangements(pattern_no, index + 1)
            else:
                self.edgeArr.append(pattern_no)


####################################################################################################  

    def non_edge_count(self, mineGrid):
        count = 0
        for i in range(len(mineGrid)):
            for j in range(len(mineGrid[i])):
                if not mineGrid[i][j].open and not mineGrid[i][j].edge:
                    count += 1
        return count    

####################################################################################################

    def product_range(a, b):
        prd = a
        i = a
        while i < b:
            i += 1
            prd *= i
        return prd

####################################################################################################


    def combinations(self, n, r):
        if n == r or r == 0:
            return 1
        else:
            if r < n - r:
                r = n - r
        return self.product_range(r + 1, n) // self.product_range(1, n - r)

####################################################################################################

    def probability_calculation(self, edge_arr, mine_grid, all_probability): # 수정요망 # 수정완
        arr_count = 0
        non_edge = self.non_edge_count(mine_grid)
        all_probability = self.allProbability

        for k in range(len(edge_arr)):
            mines_placed = 0
            for i in range(len(edge_arr[k])):
                if edge_arr[k][i].mine:
                    mines_placed += 1

            remaining_mines = self.numberofMines - mines_placed - self.hundredCount

            if 0 <= remaining_mines <= non_edge:
                non_edge_combinations = self.combinations(non_edge, remaining_mines)
                for i in range(len(edge_arr[k])):
                    if edge_arr[k][i].mine:
                        mine_grid[edge_arr[k][i]['r']][edge_arr[k][i]['c']].mineArr += non_edge_combinations
                arr_count += non_edge_combinations
                for i in range(len(mine_grid)):
                    for j in range(len(mine_grid[i])):
                        if not self.mine_grid[i][j].open and not self.mine_grid[i][j].edge:
                            self.mine_grid[i][j].mineArr += remaining_mines / non_edge * non_edge_combinations

        for i in range(len(mine_grid)):
            for j in range(len(mine_grid[i])):
                if mine_grid[i][j].edge and mine_grid[i][j].probability < 0:
                    edge_probability = round(mine_grid[i][j].mineArr / arr_count * 100)
                    if not all_probability and (edge_probability == 100 or edge_probability == 0):
                        mine_grid[i][j].probability = edge_probability
                    if all_probability:
                        mine_grid[i][j].probability = edge_probability
                if not mine_grid[i][j].open and not mine_grid[i][j].edge and mine_grid[i][j].probability < 0:
                    non_edge_probability = round(mine_grid[i][j].mineArr / arr_count * 100)
                    if not all_probability and (non_edge_probability == 100 or non_edge_probability == 0):
                        mine_grid[i][j].probability = non_edge_probability
                    if all_probability:
                        mine_grid[i][j].probability = non_edge_probability
        


####################################################################################################


    def generate_probability(self):
        # Reset old probability values 낡은 확률 청소하기
        for i in range(self.rowDimension):
            for j in range(self.colDimension):
                self.mineGrid[i][j].mineArr = 0
                self.mineGrid[i][j].probability = -1

        self.hundredCount = 0
        self.arrGrid = []
        self.edgeArr = []

        # Run basic logic rules
        self.edgeCount() # 디버깅 완료

        ret1 = True
        ret2 = True
        while ret1 or ret2:
            ret1 = self.rule_one()
            ret2 = self.rule_two()

        self.rule_three()


        # Calculate arrangements and probabilities # 이제 부터 디버깅
        index = self.find_next_edge(0, 0)
        i, j = index
        while i != -1:
            self.arrGrid.append({'mine': None, 'r': i, 'c': j})
            if j == self.colDimension - 1:
                i, j = self.find_next_edge(i + 1, 0)
                i, j = index
            else:
                i, j = self.find_next_edge(i, j + 1)
                i, j = index




        if len(self.arrGrid) > 0:
            self.generate_arrangements(self.mineGrid, self.arrGrid, 0)
            self.probability_calculation(self.edgeArr, self.mineGrid, True)

        else:
            non_edge = self.non_edge_count(self.mineGrid)
            remaining_mines = self.numberofMines - self.hundredCount
            for i in range(len(self.mineGrid)):
                for j in range(len(self.mineGrid[i])):
                    if self.mineGrid[i][j].open == False and self.mineGrid[i][j].edge == False:
                        self.mineGrid[i][j].probability = round(remaining_mines / non_edge * 100)

                        



####################################################################################################           

    def getAction(self, number: int) -> "Action Object":
        ########################################################################
        #						  MAIN				                   #
        ########################################################################
        
        #self.print_initial_grid_state() // 초기화 확인,,



        self.mineGrid[self.lastX][self.lastY].neighbors = number

        # print("last neighbor coord update: {}, {}".format(self.lastX + 1, self.lastY + 1))
        # print()

        self.generate_probability()

        
        print("Probability:")
        for i in range(self.rowDimension):
            for j in range(self.colDimension):
                # .format() 메서드를 사용하여 문자열 포매팅
                print("Cell ({}, {}): {}".format(i + 1, j + 1, self.mineGrid[i][j].probability), end=' ')
            print()
        print()


        #print("neighbors number: {}".format(number))


        # 확률이 0인 셀을 찾아 UNCOVER 액션 반환
        for i in range(self.rowDimension):
            for j in range(self.colDimension):
                if self.mineGrid[i][j].probability == 0 and not self.mineGrid[i][j].open:
                    # 확률이 0이며 아직 열리지 않은 셀을 언커버
                    
                    
                    self.lastX = i
                    self.lastY = j

                    self.mineGrid[i][j].open = True
                    
                    return Action(AI.Action.UNCOVER, i, j)
                
        
        # 확률이 0이 아닌 셀 중 가장 낮은 확률을 가진 셀 찾기
        min_probability = float('inf')  # 무한대로 초기화
        min_i, min_j = -1, -1
        for i in range(self.rowDimension):
            for j in range(self.colDimension):
                if not self.mineGrid[i][j].open and self.mineGrid[i][j].probability < min_probability and self.mineGrid[i][j].probability > 0 and not self.mineGrid[i][j].probability == 100:
                    min_probability = self.mineGrid[i][j].probability
                    min_i, min_j = i, j


        # 가장 낮은 확률의 셀을 열기
        if min_i != -1 and min_j != -1:
            self.lastX = min_i
            self.lastY = min_j
            self.mineGrid[min_i][min_j].open = True
            return Action(AI.Action.UNCOVER, min_i, min_j)


        

        # 만약 모든 셀이 처리되었거나 확률이 0인 안전한 셀이 없는 경우
        return Action(AI.Action.LEAVE)

    
########################################################################
     # def find_safe_tile(self):
    #     for x in range(self.rowDimension):
    #         for y in range(self.colDimension):
    #             if self.board_state[x][y] == 'COVERED':
    #                 neighbors = self.get_neighbors(x, y)
    #                 safe = True
    #                 for nx, ny in neighbors:
    #                     if self.board_state[nx][ny] == 'UNCOVERED':
    #                         hint_number = self.probabilities[nx][ny]
    #                         flagged_neighbors = [n for n in self.get_neighbors(nx, ny) if self.board_state[n[0]][n[1]] == 'FLAGGED']
    #                         if hint_number == len(flagged_neighbors):
    #                             safe = False
    #                             break
    #                 if safe:
    #                     return (x, y)
    #     return None

    ########################################################################

       # if len(self.uncovered_tiles) == 1:
        #     # First move, use the hint number received for the starting tile
        #     self.update_probabilities(self.startX, self.startY, number)
        # else:
        #     # Process the hint number received from the last uncovered tile
        #     last_x, last_y = self.uncovered_tiles[-1]
        #     self.update_probabilities(last_x, last_y, number)
    
      ########################################################################

      # # First, check if there are any tiles in safe_tiles list
        # while self.safe_tiles:
        #     next_x, next_y = self.safe_tiles.pop(0)
        #     if self.board_state[next_x][next_y] == 'COVERED':
        #         self.board_state[next_x][next_y] = 'UNCOVERED'
        #         self.uncovered_tiles.append((next_x, next_y))
        #         return Action(AI.Action.UNCOVER, next_x, next_y)

        # # Then, use the find_safe_tile logic
        # safe_tile = self.find_safe_tile()
        # if safe_tile is not None:
        #     next_x, next_y = safe_tile
        #     if self.board_state[next_x][next_y] == 'COVERED':
        #         self.board_state[next_x][next_y] = 'UNCOVERED'
        #         self.uncovered_tiles.append((next_x, next_y))
        #         return Action(AI.Action.UNCOVER, next_x, next_y)

        # # Find the tile with the minimum probability to uncover next
        # min_prob = float('inf')
        # max_prob = 0
        # next_move = None
        # flag_move = None

        # for x in range(self.rowDimension):
        #     for y in range(self.colDimension):
        #         if self.board_state[x][y] == 'COVERED':
        #             if self.probabilities[x][y] < min_prob:
        #                 min_prob = self.probabilities[x][y]
        #                 next_move = (x, y)
        #             if self.probabilities[x][y] > max_prob:
        #                 max_prob = self.probabilities[x][y]
        #                 flag_move = (x, y)

        # if flag_move is not None and max_prob == 1.0:
        #     fx, fy = flag_move
        #     self.board_state[fx][fy] = 'FLAGGED'
        #     self.flagged_tiles.append((fx, fy))
        #     return Action(AI.Action.FLAG, fx, fy)

        # if next_move is not None:
        #     next_x, next_y = next_move
        #     self.board_state[next_x][next_y] = 'UNCOVERED'
        #     self.uncovered_tiles.append((next_x, next_y))
        #     return Action(AI.Action.UNCOVER, next_x, next_y)

 ########################################################################


    # def get_neighbors_to_solve_1(self, x, y):
    #     neighbors = self.get_neighbors(x, y)

    #      # '?' 상태인 이웃 타일들의 수를 세기
    #     covered_neighbors_count = sum(1 for nx, ny in neighbors if self.board_hintNum[ny][nx] == '?')
    #     return covered_neighbors_count

    # def update_probabilities(self, x, y, hint_number):
    #     neighbors = self.get_neighbors(x, y)
    #     covered_neighbors = [n for n in neighbors if self.board_state[n[0]][n[1]] == 'COVERED']
    #     flagged_neighbors = [n for n in neighbors if self.board_state[n[0]][n[1]] == 'FLAGGED']
        
    #     if len(covered_neighbors) == 0:
    #         return
        
    #     prob_mine = (hint_number - len(flagged_neighbors)) / len(covered_neighbors)
        
    #     for nx, ny in covered_neighbors:
    #         self.probabilities[nx][ny] = max(self.probabilities[nx][ny], prob_mine)
        
    #     # If the hint number is 0, add all covered neighbors to safe_tiles
    #     if hint_number == 0:
    #         for nx, ny in covered_neighbors:
    #             if (nx, ny) not in self.safe_tiles:
    #                 self.safe_tiles.append((nx, ny))

 ########################################################################
