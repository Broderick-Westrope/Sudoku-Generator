from sudoku import Sudoku
from random import shuffle
from os import system


def generator(sudoku: Sudoku() = Sudoku()) -> None:
    s = Sudoku(defaultSymbol=sudoku.defaultSymbol)
    createIndependentSubmatrices(s)
    s.printSudoku()
    bruteForceFilling(s)


def createIndependentSubmatrices(s):
    values = list(range(1, 10))
    shuffle(values)
    offsets = [0, 3, 6]
    shuffle(offsets)
    while len(offsets) > 0:
        offset = offsets.pop(0)
        for v in range(9):
            s.sudoku[(v//3)+offset][(v % 3)+offset] = values[v]


def bruteForceFilling(s: Sudoku()) -> bool or None:
    """Brute-force recursive function to fill remaining cells. Creates a sudoku, s, with clues through use of random selections and brute-force backtracking. Returns True when a solution is found, otherwise returns None."""
    # If true, we have solved the system and need to return True
    system("cls")
    s.printSudoku()
    if s.isSolved():
        return True
    for row in range(s.dim[0]):
        for col in range(s.dim[1]):
            # If the cell doesn't hold the defaultSymbol, then it is already used so we should skip the cell
            if s.sudoku[row][col] != s.defaultSymbol:
                continue
            v = s.getValidValues((row, col))
            for val in list(v):
                s.sudoku[row][col] = val
                if bruteForceFilling(s):
                    return True
                s.sudoku[row][col] = s.defaultSymbol


generator()
