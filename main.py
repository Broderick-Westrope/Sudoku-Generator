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
    s = Sudoku()
    result = badGenerator(s, 17)
    s.printSudoku()


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
        value = choice(s.getValidValues(coord))
        s.setCell(coord, value)
        badGenerator(s, n)


if __name__ == '__main__':
    menu()
