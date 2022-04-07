# This algorithm combines the previously used "independence generator" with Crooks algorithm for solving sudoku's which can be found at:
# Cornells very helpful Write-Up on the algorithm - http://pi.math.cornell.edu/~mec/Summer2009/meerkamp/Site/Solving_any_Sudoku_II.html
# The original paper “A Pencil-and-Paper Algorithm for Solving Sudoku Puzzles” - http://www.ams.org/notices/200904/rtx090400460p.pdf
# The medium article where i first found the algorithm - https://towardsdatascience.com/solve-sudoku-more-elegantly-with-crooks-algorithm-in-python-5f819d371813

from sudoku import Sudoku
from random import shuffle
# import numpy as np


def generate(s: Sudoku()) -> None:
    initialMarkup = [[None for _ in range(s.dim[1])] for _ in range(s.dim[0])]
    markupCells(s, initialMarkup)


def markupCells(s: Sudoku(), markup: list) -> None:
    # If a cell only has a single markup we fill it in immediately

    # TODO - Remove these after finishing algorithm
    s.printSudoku()
    printSudoku(markup)
    # This counts how many cells we will on each run of this function. This allows us to tell when we have stopped making changes.
    fillCount = 0
    # For each cell in the sudoku
    for row in range(s.dim[0]):
        for col in range(s.dim[1]):
            # If the cell is taken, we fill it with an asterisk so we don't use it
            if s.sudoku[row][col] != s.defaultSymbol:
                markup[row][col] = '*'
            else:
                # If the cell is not taken we get a list of possible values
                values = list(s.getValidValues((row, col)))
                # If there is only one possible value then we know that must be the result
                if len(values) == 1:
                    # Place the value in the cell
                    s.sudoku[row][col] = values.pop()
                    # Block out the cell in out markup
                    markup[row][col] = '*'
                    # Increment the counter because we made a change
                    fillCount += 1
                    continue
                # If there are no values then the matrix is unsolveable from this point
                # TODO - Introduct backtracking here to avoid unnecessary 'unsolvable' sudoku
                elif len(values) == 0:
                    print("Unsolvable")
                markup[row][col] = values
    # Return if we solved the sudoku
    if s.isSolved():
        return
    # Avoid preemptive calculations until we are no longer making changes due to its high complexity (in comparison to markupCells)
    elif fillCount == 0:
        # Perform preemptive calculations
        result = preemptiveCalculations(markup)
        # If we got no result, fill random cells
        if result == False:
            fillRandomCell(s)
        # Otherwise, apply the result to the sudoku
        else:
            s.sudoku[result[1]][result[2]] = result[0]
            print("Added " + str(result[0]) +
                  " to " + str((result[1], result[2])))
            # exit("F")
    # ! Figure out how to remove this infinite loop without compromising algorithm
    markupCells(s, markup)


def preemptiveCalculations(markup: list) -> tuple or False:
    """This function attempts to find a preemptive set P and value set V. For all values x in P, x is a coordinate tuple. For all values y in V, y is an integer between 1 and 9 inclusive. The cardinality of P is equal to that of V (ie. |P|=|V|). This means, according to the occupancy law, each integer, y, must be the value of exactly one cell, x, when all cells x in P are in the same row, column, or submatrix."""
    result = None
    # For each cell in the markup
    for targetRow in range(len(markup)):
        for targetColl in range(len(markup[0])):
            # If the cell is empty
            if markup[targetRow][targetColl] != '*':
                # Create a list with all markups of the row and check it
                rowMarkups = getRow(markup, (targetRow, targetColl))
                # TODO add this kind of line to all. no point calculating when there are so many options since we cannot possibly get find P
                # if len(result) > 9:
                result = checkPreemptiveSet(rowMarkups, targetRow, targetColl)
                if result != None:
                    result[1] = targetRow
                    return result

                colMarkups = getCol(markup, (targetRow, targetColl))
                # Create a list with all markups of the col and check it
                result = checkPreemptiveSet(colMarkups, targetRow, targetColl)
                if result != None:
                    result[2] = targetColl
                    return result

                subMarkups = getSubmatrix(markup, (targetRow, targetColl))
                # Create a list with all markups of the submatrix and check it
                result = checkPreemptiveSet(subMarkups, targetRow, targetColl)
                if result != None:
                    result[1] = (targetRow-(targetRow % 3)) + (result[1]//3)
                    result[2] = (targetRow-(targetRow % 3)) + (result[1] % 3)
                    return result
    return False


def checkPreemptiveSet(markups: list, cellCheckRow, cellCheckCol):
    # For each markup in the list
    for markupPre in range(len(markups)):
        if markups[markupPre] == '*':
            continue
        # If the cardinality of the markup == the occurrences of the markup, its a preemptive set
        if len(markups[markupPre]) == markups.count(markups[markupPre]):
            # Then, for each of the markups in the list (again)
            for markupRes in range(len(markups)):
                if markups[markupRes] == '*':
                    continue
                # Find the markup minus the preemptive set
                listDiff = [x for x in markups[markupRes]
                            if x not in markups[markupPre]]
                # If there is only one value in the difference we know it must be the value due to the occupancy theorem
                if len(listDiff) == 1:
                    # We return the value and the coordinates. Although, the coordinates are different depending on whether we are checking a row, col, or submatrix, so we fix it up after returning
                    return [listDiff.pop(), markupRes, markupRes]

    # preSet is a set of numbers between 1 and 9 (inclusive) of cardinality 1<|preset|<9, so preset is of size 2-8 (inclusive)
    # we also have a list of cells, cells, which is of the same size as preSet
    # preSet represents the possible values for each cell in its corresponding list of cells


def getRow(markup, coord) -> list:
    return markup[coord[0]]


def getCol(markup, coord) -> list:
    col = []
    for row in range(len(markup)):
        col.append(markup[coord[0]])
    return col


def getSubmatrix(markup, coord) -> list:
    """Returns the values in the submatrix (3x3 cell group) of the given coordinate, coord."""
    sub = []
    startingRow = coord[0]-(coord[0] % 3)
    startingCol = coord[1]-(coord[1] % 3)
    for row in range(startingRow, startingRow+3):
        for col in range(startingCol, startingCol+3):
            sub.append(markup[row][col])
    return sub


def fillRandomCell(s: Sudoku()) -> None:
    rows = list(range(s.dim[0]))
    shuffle(rows)
    cols = list(range(s.dim[1]))
    shuffle(cols)
    for row in rows:
        for col in cols:
            if s.sudoku[row][col] == s.defaultSymbol:
                values = list(s.getValidValues((row, col)))
                shuffle(values)
                print(str(len(values)))
                if len(values) == 0:
                    ValueError(
                        str((row, col)) + " somehow had no possible values. values="+str(values))
                s.sudoku[row][col] = values.pop()
                return


def printSudoku(s) -> None:
    """Prints the sudoku to the CLI"""
    dim = list((len(s), len(s[0])))
    dim[0] = int(dim[0]+(dim[0]//4))
    val = spacer = 0
    for i in range(dim[0]):
        for j in range(dim[1]):
            if (i+1)/4 == (i+1)//4 and i != dim[0]-1:
                val, spacer = "--", "-+"
            else:
                val, spacer = ' ' + str(s[i-(i//4)][j]), " |"
            print(val, end='')
            if (j+1)/3 == (j+1)//3 and j != dim[1]-1:
                print(spacer, end='')
        print('')
    print('')
