from sudoku import Sudoku
from random import choice
from os import system


def generate(sudoku: Sudoku(), clues: int = 17) -> None:
    """Generates a complete sudoku, building on the given sudoku, if possible, then removes random values (clues) until the desired number of clues are left."""
    if not bruteForceGenerator(sudoku):
        print("Solution not found.")
    else:
        print("Solution found!!")
        if reduceSolution(sudoku, sudoku.dim[0]*sudoku.dim[1], clues):
            print("Solution reduced.")


def bruteForceGenerator(s: Sudoku()) -> bool or None:
    """Brute-force recursive generator. Creates a sudoku, s, with clues through use of random selections and brute-force backtracking. Returns True when a solution is found, otherwise returns None."""
    system("cls")
    s.printSudoku()
    # If true, we have solved the system and need to return True
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
                if bruteForceGenerator(s):
                    return True
                s.sudoku[row][col] = s.defaultSymbol


def reduceSolution(s: Sudoku(), currentClues: int, targetClues: int = 17) -> None:
    """Given a complete sudoku, s, this removes clues until there are targetClues left."""
    # If this is true we have returned the system to the desired incomplete state, so we are done
    if currentClues == targetClues:
        return True
    while(True):  # Loop choosing random cells to empty until we choose one that is not empty already
        row, col = choice(range(s.dim[0])), choice(
            range(s.dim[1]))
        if s.sudoku[row][col] != s.defaultSymbol:
            s.sudoku[row][col] = s.defaultSymbol
            if reduceSolution(s, currentClues-1):
                return True
