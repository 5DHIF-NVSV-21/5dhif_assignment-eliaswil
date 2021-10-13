## strategies ##
# https://www.sudokuwiki.org/
# https://sudoku9x9.com/sudoku_solving_techniques_9x9.html
# geeksforgeeks.com 
##


from typing import *
import time
import os

RESET = '\033[0m'
OKCYAN = '\033[96m'
FAIL = '\033[91m'
BLINK = '\033[5m'

Grid = List[List[int]]


class Sudoku:
    
    #region <basic>

    def __init__(self, sudoku_string :str, N=9):
        '''
        *args: \n
            - sudoku_string (str): All the numbers in a sudoku (0 for empty cells)
            - N (int): The Size of the Sudoku (number of cells per row|column)
        '''
        if len(sudoku_string) != N*N:
            raise ValueError('Sudoku-String must be exactly N*N long!')

        self.rows :Grid = [list(map(int, list(sudoku_string[i:i+9]))) for i in range(0, len(sudoku_string), 9)]
        self.N = N

    def __str__(self) -> str:
        '''print sudoku in pretty format'''

        output :str = '\n'
        for i in range(0, len(self.rows)):
            if i % 3 == 0 and i > 0:
                output += '-' * 21 + '\n'
            for j in range(0, len(self.rows[i])):
                if j % 3 == 0 and j > 0:
                    output += '| '
                output += str(self.rows[i][j]) + ' '
            output += '\n'
        return output

    def print_string(self):
        '''converts all the rows into a single string of numbers'''
        return ''.join([str(x) for y in self.rows for x in y])

    def print_to_file(self, filename :str):
        '''prints the sudoku (in pretty format) into a given file
        
            *args:\n
                filename (str): the name of the file (location/path)
        '''

        with open(filename, 'w') as f:
            f.write(self.__str__())
        pass

    #endregion

    #region <helper methods>

    def get_cols(self):
        # "transpose matrix" (swap rows <-> columns)
        cols = [[self.rows[row_index][col_index]] for col_index in range(len(self.rows[0])) for row_index in range(len(self.rows))]

        # flatten ([[1],[2]] -> [1,2])
        cols = [cols[i][0] for i in range(len(cols))] 

        #split into groups of 9 elements
        cols :Grid = [cols[i:i+9] for i in range(0, len(cols), 9)]
        return cols

    def get_block_id_by_coordinates(self, y :int,x :int):
        '''
        *args \n
            y (int): the row-id
            x (int): the column-id
        '''



        '''
            y, x -> id
            0, 0 -> 0
            0, 1 -> 0
            0, 2 -> 0
            0, 3 -> 1
            0, 4 -> 1
            0, 5 -> 1
            0, 6 -> 2
            0, 7 -> 2
            0, 8 -> 2
            1, 0 -> 0
            1, 1 -> 0
            1, 2 -> 0
            1, 3 -> 1

            int(y/3) -> {0,1,2}
            int(x/3) -> {0,1,2}

            0, 0 -> 0
            0, 1 -> 1
            0, 2 -> 2
            1, 0 -> 3
            1, 1 -> 4
            1, 2 -> 5
            2, 0 -> 6
            2, 1 -> 7
            2, 2 -> 8

            int(y%3)*3 -> {0,3,6}
            int(x%3) -> {0,1,2}

            id = y+x

        '''

        y, x = int(y/3), int(x/3)
        id :int = int(y%3) * 3 + int(x%3)

        return id

    def get_block_by_index(self, index :int):
        '''Returns the (9) numbers of a block, given by an index'''

        block :list[int] = []

        ''' 
            index : [start_row;end_row] [start_col;end_col]
            0: [0;3] [0;3]
            1: [0;3] [3;6]
            2: [0;3] [6;9]
            3: [3;6] [0;3]
            4: [3;6] [3;6]
            ....
        '''

        start_row_index = int(index/3) * 3
        start_col_index = (index % 3) * 3

        for i in range(start_row_index, start_row_index + 3):
            for j in range(start_col_index, start_col_index + 3):
                block.append(self.rows[i][j])

        return block

    
    def get_number_of_empty_cells(self):
        '''converts all non-zero values to 1 and sums them up'''

        '''
            0 -> 1 | 0 ** 0
            1 -> 0 | 0 ** 1
            2 -> 0 | 0 ** 2
            ... -> 0
        '''
        return sum(list(map(lambda x: 0**x, [c for r in self.rows for c in r])))

    def is_number_possible(self, number :int, row_id :int, column_id :int):
        '''checks whether a number is possible at a given place
        
        *args:\n
            number (int): the number {1-9}
            row_id (int): the index of the row {0-8}
            column_id (int): the index of the column {0-8}
        '''



        if self.rows[row_id][column_id] > 0:
            return False

        if number in self.rows[row_id]:
            return False
        if number in self.get_cols()[column_id]:
            return False
        if number in self.get_block_by_index(self.get_block_id_by_coordinates(row_id, column_id)):
            return False

        return True
    

    def generate_cell_coordinates_of_block(self, block_id :int):
        ''' is used to generate a coordinate pair (y,x) for each cell'''
        '''
        0: 0;0, 1;0, 2;0
        1: 0;3, 1;3, 2;3
        2: 0;6, 1;6, 2;6
        3: 3;0, 4;0, 5;0
        4: 3;3, 4;3, 5;3
        '''

        start_y = int(block_id/3) * 3
        start_x = (block_id % 3) * 3

        pairs :list[tuple(int, int)] = []

        for y in range(start_y, start_y + 3):
            for x in range(start_x, start_x + 3):
                pairs.append((y, x))

        return pairs

    #endregion

    pass


class Sudoku_Solver:

    def __init__(self, sudoku :Sudoku):
        self.sudoku :Sudoku = sudoku
    
    def solve(self):
        print(self.sudoku)
        t0 :float = time.time()
        while True:
            no_found_numbers :int = self.find_singles()
            # no_found_numbers :int = 0
            
            empty_cells :int = self.sudoku.get_number_of_empty_cells()
            print(no_found_numbers, empty_cells)

            if empty_cells == 0:
                break

            if no_found_numbers == 0:
                self.brute_force(self.sudoku)
                print(OKCYAN, self.sudoku, RESET)
                break

        t1 :float = time.time()
        print('\033[33m Total execution time: ', t1-t0, RESET)

    


    #region <logical solving methods>

    def find_singles(self):
        ''' tries to find as many singles as possible (row-, column- and blockwise)
        
            returns:\n
                int: number of found singles
        '''

        print('-- using: find_singles() --')
        t0 :float = time.time()
        
        no_found_singles :int = 0

        for number in range(1, self.sudoku.N + 1):

            for _id in range(self.sudoku.N):

                # ---- block ----
                possible_places_in_block :list(tuple(int, int)) = self.get_possible_places_in_block(_id, number)

                # if number fits only in one cell
                if len(possible_places_in_block) == 1:
                    self.sudoku.rows[possible_places_in_block[0][0]][possible_places_in_block[0][1]] = number
                    no_found_singles += 1

                # ---- row ----

                possible_places_in_row :list[int] = self.get_possible_places_in_row(_id, number)
                if len(possible_places_in_row) == 1:
                    self.sudoku.rows[_id][possible_places_in_row[0]] = number
                    no_found_singles += 1

                # ---- column ----
                possible_places_in_column :list[int] = self.get_possible_places_in_column(_id, number)
                if len(possible_places_in_column) == 1:
                    self.sudoku.rows[possible_places_in_column[0]][_id] = number
                    no_found_singles += 1

            pass
        
        t1 :float = time.time()
        print('  Execution Time for "Find_Singles()": ', t1-t0)

        return no_found_singles

    def get_possible_places_in_block(self, block_id, number):
        block :list[int] = self.sudoku.get_block_by_index(block_id)

        # if number is already in the block -> not possible to place it here
        if number in block:
            return []

        cell_coordinates :list(tuple(int, int)) = self.sudoku.generate_cell_coordinates_of_block(block_id)
        possible_places :list[tuple(int, int)] = []

        for cell in cell_coordinates:

            # number is already in the row
            if number in self.sudoku.rows[cell[0]]:
                continue

            # if there is already a number in this cell
            if self.sudoku.rows[cell[0]][cell[1]] != 0:
                continue

            # number is already in the column
            if number in self.sudoku.get_cols()[cell[1]]:
                continue

            # else: number can be placed here
            possible_places.append(cell)

        return possible_places

    def get_possible_places_in_row(self, row_id, number):
        if number in self.sudoku.rows[row_id]:
            return []

        possible_places :list[int] = [] # list of possible x coordinates
        columns :Grid = self.sudoku.get_cols()

        for x in range(self.sudoku.N): # 0-9
            if number in columns[x]:
                continue

            # if there is already a number in this cell
            if self.sudoku.rows[row_id][x] != 0:
                continue

            # if number in block
            if number in self.sudoku.get_block_by_index(self.sudoku.get_block_id_by_coordinates(row_id, x)):
                continue

            # else
            possible_places.append(x)

        return possible_places

    def get_possible_places_in_column(self, column_id, number):
        columns = self.sudoku.get_cols()

        if number in columns[column_id]:
            return []

        possible_places :list[int] = [] # list of possible y coordinates

        for y in range(self.sudoku.N): # 0-9
            if number in self.sudoku.rows[y]:
                continue

            # if there is already a number in this cell
            if self.sudoku.rows[y][column_id] != 0:
                continue

            # if number in block
            if number in self.sudoku.get_block_by_index(self.sudoku.get_block_id_by_coordinates(y, column_id)):
                continue

            # else
            possible_places.append(y)

        return possible_places

    #endregion
    
    #region <brute force>

    def brute_force(self, sudoku):
        ''' solves the given sudoku using the `back tracking` algorithm'''


        print('--- using back_tracking() ---')
        t0 :float = time.time()

        result :bool = self.back_tracking(sudoku)

        t1 :float = time.time()
        if not result: print(BLINK, FAIL, '\n!!!!! There is no solution to this sudoku !!!!!', RESET)
        print('  Execution time for back_tracking: ', t1-t0)

    def back_tracking(self, sudoku :Sudoku, row :int = 0, column :int = 0, level :int = 0) -> bool:
        ''' the back tracking algorithm (recursive)

        *args:\n
            sudoku (Sudoku): the sudoku object
            row (int): the current row index
            column (int): the current column index
            level (int): at which level the recursion is (only used for debugging)

        returns:\n
            bool: whether a solution was found or not

        '''

        if row == sudoku.N-1 and column == sudoku.N:
            return True

        if column == sudoku.N:
            row += 1
            column = 0

        if sudoku.rows[row][column] > 0:
            return self.back_tracking(sudoku, row, column+1, level+1)

        for number in range(1, sudoku.N + 1):
            if sudoku.is_number_possible(number, row, column):
                sudoku.rows[row][column] = number

                if self.back_tracking(sudoku, row, column + 1, level+1):
                    return True

            sudoku.rows[row][column] = 0

        return False

    #endregion




def main():

    # region <sudokus> (by sudoku.com)
    sudoku_string = '002080050300105900800000000410052000008000700000860042000000003001608009070040600'
    sudoku_string = '000672008600801700820500361000415807374900050180063900006157200000200000200090500'
    sudoku_string_easy = '000040870001000349743890056000910027400007910007004003370060090120538700065000030'
    sudoku_string_medium = '090003024000400100002000007026070005800340070403006900209060300080102040700000600'
    sudoku_string_hard = '000005902200000085000908370090602000020830000063000800006000000405300000082057090'
    sudoku_string_expert = '000091080000003010000000274080000002001000600090605000200070800704100000000040000' # even hard to brute-force
    sudoku_string_evil = '037080009006000000000100800600030000053400070100000005000002040098010007500000000' # hard for brute-force only
    #endregion

    os.system('') # activate coloring ;)


    try:
        sudoku = Sudoku(sudoku_string_evil)
        solver = Sudoku_Solver(sudoku)
        solver.solve()

        sudoku.print_to_file('solved_sudoku.txt')
    
        print('\nsudokustring: ', sudoku.print_string())

    except Exception as e:
        print(FAIL, e, RESET)
    
    pass

if __name__ == '__main__':
    main()