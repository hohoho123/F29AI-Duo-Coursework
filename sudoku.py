import sys
import time 

# A class to organise all solving methods
class sudokusolver:
    def __init__(self):
        self.grid = None
        self.steps = 0
        self.backtrack = 0
        self.starttime = 0

    #Find all valid number for a specific cell
    def getPossValues(self, row, col):
        #if cell is already filled with a number
        if self.grid[row][col] != 0:
            #return empty
            return set()
        
        #start finding all possible number from 1 - 9 
        possibleValues = set(range(1, 10))

        #Row Constraint, get numbers already in the row and convert to set
        rowValues = set(self.grid[row])

        #Column Constraint, get numbers already in the column and set comprehension for column values
        colValues = {self.grid[x][col] for x in range(9)}

        #Region Constraint, get numbers used in the 3x3 subgrid
        #Find the starting position of the 3x3 subgrid
        subGridRows, subGridCols = 3 * (row // 3), 3 * (col // 3)
        #set comprehension for subgrid values
        subGridValues = {self.grid[x][y]
                         #iterate through subgrid rows
                         for x in range(subGridRows, subGridRows + 3)
                         #iterate through subgrid column
                         for y in range(subGridCols, subGridCols + 3)
                         }
        
        #Use set difference to remove all conflicting values at once
        possibleValues -= rowValues
        possibleValues -= colValues
        possibleValues -= subGridValues
        #Remove 0 (empty cell marker) if exist
        possibleValues.discard(0)

        #Return the set of numbers that can go in the specific cell
        return possibleValues
    
    #this function decides which empty cells to fill up next, by picking the cell with FEWEST options and (harder cell)
    #fewer option for a cell indicate exist a strong constraint in that cell, therefore the fewer choices you have, harder to make wrong decision.
    def findNextCell(self): 
        #keep track of the difficult cell that was found
        bestCell = None 
        #track the minimum number of options (start with high number) 
        cellOptions = 10 
        #Flag any empty cells remain 
        emptyCellsExist = False  
        
        #Look for every cell in the Grid
        for row in range(9):  
            for col in range(9): 
                #check if cell is empty, if YES 
                if self.grid[row][col] == 0:  
                    #mark that we found an empty cell
                    emptyCellsExist = True
                    #then find what are the numbers we can put into this cell by using the getPossValue function.
                    options = self.getPossValues(row, col)  

                    #Early failure detection: if any cell has no valid options, such that no number can fit into the specific cell
                    if len(options) == 0:
                        #Signal the puzzle is unsolvable
                        return None  
                    
                     #If the cell has fewer options than our current best
                    if len(options) < cellOptions: 
                        #update our minimum options count
                        cellOptions = len(options)  
                        #remember the cell as our new best choice
                        bestCell = (row, col)  
        
        # If no empty cells exist, puzzle is completed and fully solved!
        if not emptyCellsExist:  
            return "Puzzle Solved!"  
        
        #return to the cell with the fewest options
        return bestCell  
    
    #The main recursive function that solves the puzzle
    def solve(self):  
        #find the best empty cell to try filling next
        cell = self.findNextCell() 

        #If no empty cells remain, puzzle is completed
        if cell == "Puzzle Solved!":  
            return True
        
        #If cell returned None, means we hit an unsolvable state, need to backtrack
        if cell is None:  
            return False  
        
        #Extract the row and column from the cell 
        row, col = cell  
        #Get all valid numbers for this cell
        cellPossibleValues = self.getPossValues(row, col)  
        
        #Try each possible value in that cell, one at a time
        for value in sorted(cellPossibleValues):
            #Count the number of attempt
            self.steps += 1
            #temporarily place the value in that cell  
            self.grid[row][col] = value 
            
            #RECURSION 
            #Try to solve the rest of the puzzle recursively, using that choice of value
            #If the recursive call succeeded, this value lead to a solution
            if self.solve():  
                return True  
            
            #If that didn't work, we need to backtrack
            self.backtrack += 1 
            #Remove the value that was placed temporary in that cell
            self.grid[row][col] = 0  
        
        #None of the possible values worked, so return failure
        return False  
    
    #Main public function of the entire solving process of Sudoku puzzle, with performance tracking
    def solvePuzzle(self, grid):
        #Make a copy of the puzzle, so it don't mess up the original  
        self.grid = [row[:] for row in grid]  

        #Reset all the counters
        self.steps = 0  
        self.backtrack = 0
        #start the timer  
        self.starttime = time.time()  
        
        #Attempting to solve the puzzle by using the function created!
        success = self.solve() 
        #Record the time taken to finish solving
        endtime = time.time()  
        
        return {
            #whether we successfully solved it 
            'solved': success,
            #the final state of the grid (solved or partial)
            'grid': self.grid, 
            #total number of placement attempts made 
            'steps': self.steps,
            #total number of times to undo a cell
            'backtracks': self.backtrack, 
            #Execution time in milliseconds 
            'time_ms': (endtime - self.starttime) * 1000  
        }
    
    #A Function to display the 9x9 Sudoku Grid Format
    def printGrid(self, grid): 
        #print a top border line 
        print("\n" + "-" * 22)  
        #iterate each row with its index number
        for i, row in enumerate(grid):  
             #Every 3rd row, print a separator line (to show the 3x3 boxes)
            if i % 3 == 0 and i != 0:
                print("------+-------+------")  
            
            rowdivider = ""  
            #iterate through each number with its index
            for j, num in enumerate(row):  
                #Every 3rd column, add a vertical separator
                if j % 3 == 0 and j != 0:  
                    rowdivider += "| " 
                rowdivider += f"{num if num != 0 else '.'} " 

            # Print the completed row 
            print(rowdivider)  
        # Print a bottom border line
        print("-" * 22)  

#File Reader Function, Read a 9x9 Sudoku Puzzle from a text file
def boardReader(filename):  
    #Initialize an empty list to store the board
    board = []  
    
    #Open the file, and read line by line
    with open(filename, 'r') as file:  
        for line in file:  
            #Remove any extra whitespace from the line
            line = line.strip() 
            #If the line is not empty,
            if line:  
                #clean up the line format (remove brackets and commas) and extract numbers
                line = line.replace('[', '').replace(']', '').replace(',', ' ') 
                #split the line into individual numbers  
                numbers = line.split()  
                
                #If exactly 9 numbers are found, therefore is a valid Sudoku Row
                if len(numbers) == 9:  
                    #convert each string number into an integer
                    row = [int(num) for num in numbers]  
                    #Then, add this row to our board
                    board.append(row)  
    
    #If the row doesnt have 9 numbers, raise an error because it's not a valid Sudoku Puzzle
    if len(board) != 9:  
        raise ValueError("Sudoku Board must be in a 9x9 cell format.")  
    
    return board 

#Only run this code if the file is executed directly (not imported)
if __name__ == '__main__': 
    #Check if the user provided a filename
    if len(sys.argv) != 2: 
        #Show them how to use the program
        print("Usage: python sudoku.py board.txt")  
        #Exit with error
        sys.exit(1)  
    
    try:  
        #Try to load the puzzle from the file the user specified
        board = boardReader(sys.argv[1])  
        #Create a new instance of our solver
        solver = sudokusolver()  
        
        print("Here is the Original Puzzle:")  
        #Display the unsolved puzzle the Sudoku Format 
        solver.printGrid(board)  
        
        #Solve the puzzle and measure performance
        print("\nThe algorithm is currently solving the Sudoku Puzzle...") 
        result = solver.solvePuzzle(board)  
        
        #If the solver successfully found a solution
        if result['solved']:  
            print("\nSudoku Puzzle Solved Successfully!") 
            #Display the results in the Sudoku Grid Format
            solver.printGrid(result['grid'])  
            
            # Label for the metrics
            print(f"\nPerformance Metrics:")  
            print(f"Total Steps Taken: {result['steps']}")  
            print(f"Numbers of Backtracks: {result['backtracks']}")  
            print(f"Execution time: {result['time_ms']:.1f} ms")  

        #If the solver could not find a solution           
        else:  
            print("\nNo solution found.")  
            print("The puzzle may be invalid or unsolvable") 

    #Exception Handling        
    except Exception as e:
        print(f"Error: {e}")  
