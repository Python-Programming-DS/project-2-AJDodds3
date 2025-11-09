'''
My name is Andrew Dodds and this program was developed on 11/1/2025

The purpose of this script is to take my computerized version of Tic-Tac-Toe that has
been updated with classes and objects, and implement the Minimax algorithm to choose the best
move for the Tic-Tac-Toe computer player. Tac-Tac-Toe is a solved game and the first player will always
either win or draw if played optimally and the second player will always draw if played optimally.

Information about the algorithm was obtained from https://www.deep-ml.com/problems/171 and my key notes are below:
- Minimax algorithm is a recursive method for finding the optimal move in two-player zero-sum games
- When the algorithm is called it assumes both players play optimally 
    - One player tries to maximize their outcome
    - The other player tries to minimize the outcome
    - AI is the maximizer and me the user and opponent will be the minimizer
- Board states:
    - If X wins +1
    - If O wins -1
    - If draw: 0
- Recursion:
    - go through all possible moves and assign scores to the outcome
    - recursively call the minimax function for the new board state and the other players turn
    - If maximizing -> pick highest move, if minimizing -> pick lowest score move
'''

class Board:
    def __init__(self):
        self.gameBoard = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]] # gameBoard is a tic tac toe board

    def printBoard(self): # Display the game board
        print("-----------------")
        print(f"|R\C| 0 | 1 | 2 |")
        print("-----------------")
        print(f"| 0 | {self.gameBoard[0][0]} | {self.gameBoard[0][1]} | {self.gameBoard[0][2]} |")
        print("-----------------")
        print(f"| 1 | {self.gameBoard[1][0]} | {self.gameBoard[1][1]} | {self.gameBoard[1][2]} |")
        print("-----------------")
        print(f"| 2 | {self.gameBoard[2][0]} | {self.gameBoard[2][1]} | {self.gameBoard[2][2]} |")
        print("-----------------")
        print()

class Game:
    def __init__(self):
        self.board = Board()
        self.turn = 'X' # X goes first
        self.userInput = 'y' # user starts wanting to play
        self.gameOver = False # tracks if game is over
        self.entryValid = False # tracks if user enters a proper play
        self.entryFormat = False # makes sure the turn entry is valid
        self.boardLocation = "" # stores the user's desired position for their turn
        self.maximizing = True # Stores whether or not the minimax algorithm is maximizing or minimizing
        self.minimaxPosition = "" # Store the best possible position for the computer

    # Once the best position has been found format 
    def minimaxFormat(self, i, j):
        formatString = f"{i},{j}"
        return formatString
    
    # Call the minimax algorithm to find the best score so that the best position can be found
    def getComputersPosition(self):
        minimaxScore = -10 # Stores the score
        tempScore = -10 # Compare current score to new score to find the best move
        self.minimaxPosition = ""
        # Iterate through the board -> the computer is always maximizing in this program so test empty position with x and get the score calling minimaxRecurse
        for i in range(len(self.board.gameBoard)):
            for j in range(len(self.board.gameBoard[i])):
                if (self.board.gameBoard[i][j] == " "):
                    self.board.gameBoard[i][j] = "X" # Test the maximizing players score by placing an X at empty positions and calling minimaxRecurse to go through all possible outcomes if this test move is placed
                    self.maximizing = False # O's turn -> minimizing when minimaxRecurse is called
                    tempScore = self.minimaxRecurse()
                    self.maximizing = True # Reset the turn
                    self.board.gameBoard[i][j] = " " # board has been tested, reset for now
                    if (tempScore > minimaxScore):
                        minimaxScore = tempScore # If a better score was found using the test move and recursion, update the miniMax score and also store the current best position
                        self.minimaxPosition = self.minimaxFormat(i, j)
        return  # All possible moves have been tested, once out of the loop the best possible position should have been found
        

    # Minimax algorithm
    def minimaxRecurse(self):
        # Need to check the board states as a way to exit the recursion (check if X won or if O won or the board if full and its a draw +1 -1 0)
        turnStorage = self.turn
        self.turn = 'X'
        if (self.checkWin()):
            self.turn = turnStorage
            return 1
        self.turn = 'O'
        if (self.checkWin()):
            self.turn = turnStorage
            return -1
        if (self.checkFull()):
            self.turn = turnStorage
            return 0
        self.turn = turnStorage
        
        if (self.maximizing): # Maximizing
            tempScore = -10
            minimaxScore = -10
            for i in range(len(self.board.gameBoard)): # Iterate through all rows and cols of the board and if there is 1 or more empty spaces then use the minimax algorithm to assign scores to find the optimal move
                for j in range(len(self.board.gameBoard[i])):
                    # If the board is empty, then it is a possible move, so need to assign a score to it by calling minimaxRecurse -> assign all scores to all possible moves after that move and so on
                    if (self.board.gameBoard[i][j] == " "):
                        self.board.gameBoard[i][j] = "X" # maximizing players turn so temporarily place X at row, col
                        self.maximizing = False
                        tempScore = self.minimaxRecurse()
                        self.maximizing = True
                        self.board.gameBoard[i][j] = " " # Reset the board at position because it has been "tested" and there are possible other position to test
                        if (tempScore > minimaxScore): # If the score for the pass is > current winning score then replace (maximizing)
                            minimaxScore = tempScore
            return minimaxScore

        else: # Minimizing
            tempScore = 10
            minimaxScore = 10
            for i in range(len(self.board.gameBoard)):
                for j in range(len(self.board.gameBoard[i])):
                    if (self.board.gameBoard[i][j] == " "):
                        self.board.gameBoard[i][j] = "O" # minimizing players turn so  temporarily place O at row, col
                        self.maximizing = True
                        tempScore = self.minimaxRecurse()
                        self.maximizing = False
                        self.board.gameBoard[i][j] = " " 
                        if (tempScore < minimaxScore): # If the score from the pass is < current score then replace because minimizing
                            minimaxScore = tempScore   
            return minimaxScore

    def switchPlayer(self): # Switches the player
        if self.turn == "X": # X goes to O and O goes to X at the end of a turn
            self.turn = "O"
        else:
            self.turn = "X"

    """
    validateEntry(self, row, col): returns True if the user entered inputs are valid, otherwise returns False.
    The logic behind the function is to first check if the row and col numbers as well as the location is valid.
    This is the case when the input its not 0, 1, or 2 for both row and col or not an integer.

    https://pythonguides.com/python-check-if-the-variable-is-an-integer/ 
    """

    def validateEntry(self, row, col): 
        if (row < 0 or row > 2 or col < 0 or col > 2 or not isinstance(row, int) or not isinstance(col, int)):
            print("Invalid entry: try again.")
            print("Row & column numbers must be either 0, 1, or 2.\n")
            return False
        if (self.board.gameBoard[row][col] != " "): #if there's an X or O at the row, col then cannot add anything
            print("That cell is already taken.")
            print("Please make another selection.\n")
            return False
        print("Thank you for your selection.")
        return True # Valid entry return true and then add to board
    
    def checkFull(self): # Returns True if the board is full, otherwise, returns false
        for i in range(len(self.board.gameBoard)): # Iterate through all rows
            for j in range(len(self.board.gameBoard[i])): # Iterate through all cols in a row
                if self.board.gameBoard[i][j] == " ": #I f there is an empty space in any of the rows or cols board is not full return false
                    return False
        return True # Could not find an empty space
    
    def checkWin(self): # Returns True when 'X' or 'O' becomes a winner, otherwise, returns False
        '''
        Need to iterate through all rows and cols
        User can win if they have 3 across in any row, 3 down in any col, or 3 diag
        '''
        for i in range(len(self.board.gameBoard)):
            for j in range(len(self.board.gameBoard)):
                # If a win is found return true otherwise keep iterating through the board to check for wins
                if j + 2 < len(self.board.gameBoard): # Cols to the right
                    if (self.board.gameBoard[i][j] == self.turn and self.board.gameBoard[i][j + 1] == self.turn and self.board.gameBoard[i][j + 2] == self.turn):
                        return True
                if j - 2 >= 0: # Cols to the left
                    if (self.board.gameBoard[i][j] == self.turn and self.board.gameBoard[i][j - 1] == self.turn and self.board.gameBoard[i][j - 2] == self.turn):
                        return True
                if i + 2 < len(self.board.gameBoard): # Rows below
                    if (self.board.gameBoard[i][j] == self.turn and self.board.gameBoard[i + 1][j] == self.turn and self.board.gameBoard[i + 2][j] == self.turn):
                        return True
                if i - 2 >= 0: #  Rows above
                    if (self.board.gameBoard[i][j] == self.turn and self.board.gameBoard[i - 1][j] == self.turn and self.board.gameBoard[i - 2][j] == self.turn):
                        return True
                if j + 2 < len(self.board.gameBoard) and i + 2 < len(self.board.gameBoard): # Down and to the right diag
                    if (self.board.gameBoard[i][j] == self.turn and self.board.gameBoard[i + 1][j + 1] == self.turn and self.board.gameBoard[i + 2][j + 2] == self.turn):
                        return True
                if j - 2 >= 0 and i - 2 >= 0: #  Up and to the left diag
                    if (self.board.gameBoard[i][j] == self.turn and self.board.gameBoard[i -1 ][j - 1] == self.turn and self.board.gameBoard[i - 2][j - 2] == self.turn):
                        return True
                if j - 2 >= 0 and i + 2 < len(self.board.gameBoard): # Down and to the left diag
                    if (self.board.gameBoard[i][j] == self.turn and self.board.gameBoard[i + 1][j - 1] == self.turn and self.board.gameBoard[i + 2][j - 2] == self.turn):
                        return True
                if j + 2 < len(self.board.gameBoard) and i - 2 >= 0: # Up and to the right diag
                    if (self.board.gameBoard[i][j] == self.turn and self.board.gameBoard[i - 1][j + 1] == self.turn and self.board.gameBoard[i - 2][j + 2] == self.turn):
                        return True
        return False # No win is found

    def checkEnd(self): # Returns true if a game is over, otherwise, returns False. Game is over on draw or 
        '''
        A win is a priority so first check if someone won and return if they did
        If no one won then check if the board is full and return if its a draw
        '''
        if (self.checkWin()): # If the user won print x or o winner and return true
            print()
            print(f"{self.turn} IS THE WINNER!!!")
            self.board.printBoard()
            return True
        if (self.checkFull()):  # If the board is full it is a draw and return true (gameover)
            print() 
            print("DRAW! NOBODY WINS!")
            self.board.printBoard()
            return True
        self.board.printBoard()
        return False

    def playGame(self): # Plays tic-tac-toe game by calling other methods
        while self.userInput.lower() == "y": # While user wants to play, simulate a game and repeat
            self.board = Board()
            self.turn = 'X' 
            self.userInput = 'y' 
            self.gameOver = False 
            self.entryValid = False 
            self.entryFormat = False 
            self.boardLocation = "" 
            print(f"New Game: {self.turn} goes first.\n")
            self.board.printBoard()
            while self.gameOver == False:
                while self.entryValid == False:
                    self.maximizing = True
                    self.minimaxPosition = ""
                    # If it is X's turn (the computers turn) call the minimax algorithm, get the optimal move in correct format and add to board
                    # if computer turn set entry format to true because dont need to check then self.boardlocation to the minimax format
                    if (self.turn == "X"):
                        print("It is the computer's (X's) turn.")
                        self.entryFormat = True
                        self.getComputersPosition()
                        self.boardLocation = self.minimaxPosition
                    else:
                        print(f"{self.turn}'s turn.")
                        print(f"Where do you want your {self.turn} placed?")
                        self.entryFormat = False
                    while self.entryFormat == False:
                        self.boardLocation = input("Please enter row number and column number separated by a comma.\n")
                        if (len(self.boardLocation) == 3 and self.boardLocation[0].isdigit() and self.boardLocation[1] == "," and self.boardLocation[2].isdigit()): # If the input string's length is 3, theres a digit at the first position, a comma at the 2nd position, and a digit at the third position then continue
                            self.entryFormat = True
                        else:
                            print("Invalid input")
                    if (self.turn == "X"):
                        print(f"The computer's minimax algorithm has chosen the position {self.boardLocation}")
                    self.boardLocation = self.boardLocation.split(",")
                    if (self.turn == "O"):
                        print(f"You have entered row #{int(self.boardLocation[0])}") 
                        print(f"\t  and column #{int(self.boardLocation[1])}")
                    self.entryValid = self.validateEntry(int(self.boardLocation[0]), int(self.boardLocation[1])) 
                self.board.gameBoard[int(self.boardLocation[0])][int(self.boardLocation[1])] = self.turn # Valid entry so add to board
                self.gameOver = self.checkEnd() # Determine if board is full or someone won or to continue the game
                self.switchPlayer() # Turn has been played and game is not over so switch turns
                self.entryValid = False # Prepare for a new input
            self.userInput = input("Another game? Enter Y or y for yes. \n")
        print("Thank you for playing!")
        

def main():
    ticTacToe = Game()
    ticTacToe.playGame()

if __name__ == '__main__':
    main()
