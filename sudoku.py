import csv

# This is the symbol used to represent an empty cell when one is not provided on initialization
DEFAULT_SYMBOL = ' '


class Sudoku:
    def __init__(self, defaultSymbol: str = DEFAULT_SYMBOL, importSudoku: bool = False):
        """Initializes a new Sudoku with the symbol, defaultSymbol, representing empty cells."""
        if importSudoku:
            self.importSudoku()
        else:
            self.defaultSymbol = defaultSymbol
            # Initializes a new, blank sudoku with the standard 81 cells
            self.sudoku = [[defaultSymbol for j in range(9)]for i in range(9)]
            self.dim = self.getSudokuDimensions()

    def getEmptyCellIndices(self) -> list:
        """Returns a list of tuples, each of which is a coordinate for an empty cell within the sudoku."""
        coords = []
        for i in range(len(self.sudoku)-1):
            for j in range(len(self.sudoku[0])-1):
                if self.sudoku[i][j] == self.defaultSymbol:
                    coords.append((i, j))
        return coords

    def getValidValues(self, coord: tuple) -> set:
        """Returns a list of values (from 1 to 9 inclusive) that can legally be placed in the given cell."""
        if self.sudoku[coord[0]][coord[1]] != '':
            ValueError(
                "Given coordinate was not empty. Cannot override a non-empty cell value.")
        invalidValues = set()
        # Add values in the same row to invalid set
        invalidValues = invalidValues.union(set(self.sudoku[coord[0]]))
        # Add values in the same column to invalid set
        for row in range(self.dim[1]):
            invalidValues.add(self.sudoku[row][coord[1]])
        # Add values in the same submatrix (3x3 group) to invalid set
        x = self.getSubmatrixValues(coord)
        invalidValues = invalidValues.union(x)
        # Perform the set difference between the potential and invalid values to produce the valid values
        validValues = set([str(x) for x in range(1, 10)])
        return validValues.difference(invalidValues)

    def setCell(self, coord: tuple, value: int):
        """Puts the given value at the given coordinate, coord./"""
        self.sudoku[coord[0]][coord[1]] = value

    def getSudokuDimensions(self) -> tuple:
        """Returns a tuple containing the number of rows and columns that make up the sudoku."""
        return (len(self.sudoku), len(self.sudoku[0]))

    def getSubmatrixValues(self, coord: tuple) -> set:
        """Returns the values in the submatrix (3x3 cell group) of the given coordinate, coord."""
        values = set()
        startingRow = coord[0]-(coord[0] % 3)
        startingCol = coord[1]-(coord[1] % 3)
        for row in range(startingRow, startingRow+3):
            for col in range(startingCol, startingCol+3):
                values.add(self.sudoku[row][col])
        return values

    def printSudoku(self) -> None:
        """Prints the sudoku to the CLI"""
        dim = list(self.dim)
        dim[0] = int(dim[0]+(dim[0]//4))
        val = spacer = 0
        for i in range(dim[0]):
            for j in range(dim[1]):
                if (i+1)/4 == (i+1)//4 and i != dim[0]-1:
                    val, spacer = "--", "-+"
                else:
                    val, spacer = ' ' + str(self.sudoku[i-(i//4)][j]), " |"
                print(val, end='')
                if (j+1)/3 == (j+1)//3 and j != dim[1]-1:
                    print(spacer, end='')

            print('')
        print('')

    def exportSudoku(self):
        with open('problem1', 'w') as file:
            writer = csv.writer(file)
            writer.writerows(self.sudoku)

    def importSudoku(self):
        self.sudoku = []
        with open('problem1', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                self.sudoku.append(row)
        if len(self.sudoku) <= 0:
            ValueError("Failed to import sudoku. The result was an empty list.")
        self.dim = self.getSudokuDimensions()
        self.defaultSymbol = DEFAULT_SYMBOL
        print("x=" + str(self.defaultSymbol) + "|")
        for row in range(self.dim[0]):
            for col in range(self.dim[1]):
                if not isinstance(self.sudoku[row][col], int) and not str.isdigit(self.sudoku[row][col]):
                    self.defaultSymbol = self.sudoku[row][col]
                    break
        print("Import Successful:")
        self.printSudoku()
        print("Empty Symbol: |" + str(self.defaultSymbol + "|"))

    def isSolved(self) -> bool:
        for row in range(self.dim[0]):
            for col in range(self.dim[1]):
                if not str.isdigit(str(self.sudoku[row][col])):
                    return False
        return True

        # 1 2 3 | 1 2 3 | 1 2 3
        # 1 2 3 | 1 2 3 | 1 2 3
        # 1 2 3 | 1 2 3 | 1 2 3
        # ------+-------+------
        # 1 2 3 | 1 2 3 | 1 2 3
        # 1 2 3 | 1 2 3 | 1 2 3
        # 1 2 3 | 1 2 3 | 1 2 3
        # ------+-------+------
        # 1 2 3 | 1 2 3 | 1 2 3
        # 1 2 3 | 1 2 3 | 1 2 3
        # 1 2 3 | 1 2 3 | 1 2 3
