from sudoku import Sudoku
from random import choice


def menu() -> None:
    choice = input(
        "What would you like to do?\n[C]reate a sudoku with parameters\n[G]enerate a sudoku with random parameters")
    if choice == 'C' or choice == 'c':
        createSudoku()
    elif choice == 'G' or choice == 'g':
        generateSudoku()


def createSudoku() -> None:
    """Allows the user to create a standard 81 cell sudoku with their given number of clues filled in."""
    s = Sudoku(importSudoku=True)
    # result = badGenerator(s, 17)
    # s.exportSudoku()
    result = bruteForceGenerator(s, 36)
    result.printSudoku()


def generateSudoku() -> None:
    """Generates a standard 81 cell sudoku with a random number of clues (from 17 to 80 inclusive)."""
    pass


def badGenerator(s: Sudoku(), n: int) -> Sudoku():
    """Bad recursive generator. Creates a sudoku, s, with n clues, although it cannot be guaranteed that s is solvable."""
    if n == 0:
        return s
    else:
        n -= 1
        # Selects a cell the list of coordinates (stored as coordinate tuples)
        coord = choice(s.getEmptyCellIndices())
        value = choice(list(s.getValidValues(coord)))
        s.setCell(coord, value)
        badGenerator(s, n)


def reduceSolution(s: Sudoku(), currentClues: int, targetClues: int = 17) -> Sudoku():
    """Given a complete sudoku, s, this removes clues until there are targetClues left."""
    # If this is true we have returned the system to the desired incomplete state, so we are done
    if currentClues == targetClues:
        return s
    else:
        while(True):  # Loop choosing random cells to empty until we choose one that is not empty already
            row, col = choice(range(s.dim[0])), choice(range(s.dim[1]))
            if s.sudoku[row][col] != s.defaultSymbol:
                s.sudoku[row][col] = s.defaultSymbol
                currentClues -= 1
                return reduceSolution(s, currentClues)


def bruteForceGenerator(s: Sudoku(), clues: int) -> Sudoku() or None:
    """Brute-force recursive generator. Creates a sudoku, s, with clues through use of random selections and brute-force backtracking. Returns a Sudoku when a solution is found, otherwise returns None."""
    # If true, we have solved the system and need to return the result
    if clues == s.dim[0]*s.dim[1]:
        return s
    for row in range(s.dim[0]):
        for col in range(s.dim[1]):
            # If the cell doesn't hold the defaultSymbol, then it is already used so we should skip the cell
            if s.sudoku[row][col] != s.defaultSymbol:
                continue
            for val in list(s.getValidValues((row, col))):
                s.sudoku[row][col] = val
                result = bruteForceGenerator(s, clues+1)
                if type(result) == Sudoku():
                    return result
                s.sudoku[row][col] = s.defaultSymbol


if __name__ == '__main__':
    menu()
