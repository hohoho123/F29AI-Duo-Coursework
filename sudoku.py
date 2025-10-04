import sys
from pprint import pprint

def findNextEmpty(sudoku):
    for r in range(9):
        for c in range(9):
            if sudoku[r][c] == 0:
                return r, c
            
    return None, None

def isValid(sudoku, guess, row, col):
    rowValues = sudoku[row]
    if guess in rowValues:
        return False
    
    colValues = [sudoku[i][col] for i in range(9)]
    if guess in colValues:
        return False
    
    rowStart = (row // 3) * 3
    colStart = (col // 3) * 3
    
    for r in range(rowStart, rowStart + 3):
        for c in range(colStart, colStart + 3):
            if sudoku[r][c] == guess:
                return False
    
    return True

def solveSudoku(sudoku):
    row, col = findNextEmpty(sudoku)
    
    if row is None:
        return True
    
    for guess in range(1, 10):
        if isValid(sudoku, guess, row, col):
            sudoku[row][col] = guess
            
            if solveSudoku(sudoku):
                return True
        
        sudoku[row][col] = 0
        
    return False

def readBoard(filename):
    board = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip().replace('[', '').replace(']', '')
            if line:
                row = [int(x) for x in line.split(',') if x.strip()]
                board.append(row)
    
    return board  
    

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python sudoku.py <board_file.txt>")
        sys.exit(1)
        
    board = readBoard(sys.argv[1])
        
    print(solveSudoku(board))
    pprint(board)