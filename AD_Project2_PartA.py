'''
My name is Andrew Dodds and this program was developed on 10/27/2025

The purpose of this script is to improve my computerized version of Tic-Tac-Toe
using classes and objects. I will be implementing a Board class and a game Class to 
handle logic for both running the game and updating the board. The method logic 
is copied almost exactly from my Tic Tac Toe project without classes
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
                    print(f"{self.turn}'s turn.")
                    print(f"Where do you want your {self.turn} placed?")
                    self.entryFormat = False
                    while self.entryFormat == False:
                        self.boardLocation = input("Please enter row number and column number separated by a comma.\n")
                        if (len(self.boardLocation) == 3 and self.boardLocation[0].isdigit() and self.boardLocation[1] == "," and self.boardLocation[2].isdigit()): # If the input string's length is 3, theres a digit at the first position, a comma at the 2nd position, and a digit at the third position then continue
                            self.entryFormat = True
                        else:
                            print("Invalid input")
                    self.boardLocation = self.boardLocation.split(",")
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
