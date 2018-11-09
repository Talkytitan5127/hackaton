#!/usr/bin/python3

import random
import solver
import copy

class Grid:
    def __init__(self, n=3):
        self.size = n
        self.table = [[ ((i*n + i//n + j) % (n*n) + 1) for j in range(n*n)] for i in range(n*n)]

    def pprint(self):
        for i in self.table:
            print(i)

    def transporting(self):
        self.table = list(map(list, zip(*self.table)))

    def swap_rows_small(self):
        area = random.randrange(0, self.size, 1)
        line1 = random.randrange(0, self.size, 1)
        
        N1 = area*self.size + line1

        line2 = random.randrange(0, self.size, 1)

        while line1 == line2:
            line2 = random.randrange(0, self.size, 1)
        
        N2 = area*self.size + line1

        self.table[N1], self.table[N2] = self.table[N2], self.table[N1]
    
    def swap_colums_small(self):
        self.transporting()
        self.swap_rows_small()
        self.transporting()

    def swap_rows_area(self):
        area1 = random.randrange(0, self.size, 1)
        area2 = random.randrange(0, self.size, 1)

        while area1 == area2:
            area2 = random.randrange(0, self.size, 1)

        for i in range(0, self.size):
            N1, N2 = area1*self.size + i, area2*self.size + i
            self.table[N1], self.table[N2] = self.table[N2], self.table[N1]

    def swap_colums_area(self):
        self.transporting()
        self.swap_rows_area()
        self.transporting()
    
    def mix(self, amt=10):
        mix_func = [
            self.transporting,
            self.swap_rows_small,
            self.swap_colums_small,
            self.swap_rows_area,
            self.swap_colums_area
        ]
        for i in range(1, amt):
            id_func = random.randrange(0, len(mix_func), 1)
            mix_func[id_func]()
    
    def get(self):
        self.mix()
        return self.table


class Sudoku:
    def __init__(self):
        grid = Grid()
        self.grid = grid.get()
        self.user_grid = copy.deepcopy(self.grid)
        self.size = grid.size
    
    def mix_user_grid(self):
        length = self.size*self.size
        flook = [[0]*length for i in range(length)]
        iterator = 0
        difficult = length**2
        while iterator < difficult:
            i, j = random.randrange(0, length, 1), random.randrange(0, length, 1)
            if not flook[i][j]:
                iterator += 1
                flook[i][j] = 1

                temp = self.user_grid[i][j]
                self.user_grid[i][j] = 0

                difficult -= 1

                table_solution = []
                for copy_i in range(0, length):
                    table_solution.append(self.user_grid[copy_i][:])
                
                i_solution = 0
                for solution in solver.solve_sudoku((self.size, self.size), table_solution):
                    i_solution += 1
                
                if i_solution != 1:
                    self.user_grid[i][j] = temp
                    difficult += 1


if __name__ == '__main__':
    obj = Sudoku()
    obj.mix_user_grid()
    print("USER")
    for i in obj.user_grid:
        print(i)
    print('#'*10)
    for i in obj.grid:
        print(i)