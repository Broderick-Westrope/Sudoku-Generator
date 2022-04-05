class Sudoku:
    def __init__(self):
        # Initialises a new, blank sudoku with the standard 81 cells
        self.sudoku = [['?' for j in range(9)]for i in range(9)]

    def getEmptyCellIndices(self) -> list:
        """Returns a list of tuples, each of which is a coordinate for an empty cell within the sudoku."""
        coords = []
        for i in range(len(self.sudoku)-1):
            for j in range(len(self.sudoku[0])-1):
                if self.sudoku[i][j] == '?':
                    coords.append((i, j))
        return coords

    def getValidValues(self, coord: tuple) -> list:
        """Returns a list of values (from 1 to 9 inclusive) that can legally be placed in the given cell."""
        if self.sudoku[coord[0]][coord[1]] != '':
            ValueError(
                "Given coordinate was not empty. Cannot override a non-empty cell value.")
        possibleValues = list(range(1, 10))
        # Remove row and column values
        for i in range(len(self.sudoku)-1):
            rowValue = self.sudoku[coord[0]][i]
            rowCount = possibleValues.count(rowValue)
            if rowCount == 1:
                possibleValues.remove(rowValue)
            elif rowCount > 1:
                ValueError("There was more than one instace of " +
                           self.sudoku[coord[0]][i] + " in the possible values.")

            colValue = self.sudoku[i][coord[1]]
            colCount = possibleValues.count(colValue)
            if colCount == 1:
                possibleValues.remove(colValue)
            elif colCount > 1:
                ValueError("There was more than one instace of " +
                           self.sudoku[i][coord[1]] + " in the possible values.")
        return possibleValues

    def setCell(self, coord: tuple, value: int):
        """Puts the given value at the given coordinate, coord./"""
        self.sudoku[coord[0]][coord[1]] = value

    def getSudokuDimensions(self) -> tuple:
        """Returns a tuple containing the number of rows and columns that make up the sudoku."""
        return (len(self.sudoku), len(self.sudoku[0]))

    def printSudoku(self) -> None:
        """Prints the sudoku to the CLI"""
        dim = list(self.getSudokuDimensions())
        # multiples of 8, minus 1
        # 8m-1
        dim[0] = int(dim[0]+(dim[0]//4))
        val, spacer = 0, 0
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
