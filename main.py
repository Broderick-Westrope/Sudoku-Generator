from sudoku import Sudoku


def menu():
    choice = input(
        "What would you like to do?\n[C]reate a sudoku with parameters\n[G]enerate a sudoku with random parameters")
    if choice == 'C' or choice == 'c':
        createSudoku()
    elif choice == 'G' or choice == 'g':
        generateSudoku()


def createSudoku():
    """Allows the user to create a standard 81 cell sudoku with their given number of clues filled in."""
    masterS = Sudoku()  # this master sudoku will be the sudoku we create


def generateSudoku():
    """Generates a standard 81 cell sudoku with a random number of clues (from 17 to 80 inclusive)."""
    pass


def sudokuLoop(s: Sudoku()):
    pass


if __name__ == '__main__':
    menu()
