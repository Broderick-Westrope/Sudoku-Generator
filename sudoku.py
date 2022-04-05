class Sudoku:
    def __init__(self):
        # Initialises a new, blank sudoku with the standard 81 cells
        self.sudoku = [[0 for j in range(18)]for i in range(18)]
