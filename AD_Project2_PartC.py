'''
My name is Andrew Dodds and this program was developed on 11/8/2025

The purpose of this script is to build upon my computerized version of Tic-Tac-Toe
by using one of the provided datasets to modify the game so that a human can play against
a machine learning model. I will be using tictac_single.txt which is a dataset setup so that
it is O players move. Some of the code is reused from our live coding sessions and HW 10 that showed us how
to train models.

*** Note it takes between 60-90 seconds for the model to train on start *** 
'''

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics


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
        self.prediction = "" # stores the models prediction
        self.modelInput = [] # stores the state of the board in a form the model can understand
        self.model = trainModel() # stores the trained model 

    def switchPlayer(self): # Switches the player
        if self.turn == "X": # X goes to O and O goes to X at the end of a turn
            self.turn = "O"
        else:
            self.turn = "X"

    # Set the ml input to mimic user input format
    def boardFormat(self, i, j):
        formatString = f"{i},{j}"
        return formatString
    
    # convert the prediction back to row, col form 
    def convertToBoard(self, mlMove):
        if (mlMove == 0):
            i, j = 0, 0
        elif (mlMove == 1):
            i, j = 0, 1
        elif (mlMove == 2):
            i, j = 0, 2
        elif (mlMove == 3):
            i, j = 1, 0
        elif (mlMove == 4):
            i, j = 1, 1
        elif (mlMove == 5):
            i, j = 1, 2
        elif (mlMove == 6):
            i, j = 2, 0
        elif (mlMove == 7):
            i, j = 2, 1
        else:
            i, j = 2, 2
        return self.boardFormat(i, j)
        

    def mlPredict(self):
        self.modelInput = []
        # iterate through the board and append to model input 1 for X -1 for O and 0 for empty
        for i in range(len(self.board.gameBoard)):
            for j in range(len(self.board.gameBoard[i])):
                if self.board.gameBoard[i][j] == "X":
                    self.modelInput.append(1)
                elif self.board.gameBoard[i][j] == "O":
                    self.modelInput.append(-1)
                else:
                    self.modelInput.append(0)
        # the predict expects a 2D array instead of 1D so need to convert - ValueError Reshape your data using array.reshape(-1, 1)
        tempList = np.array(self.modelInput).reshape(1, -1)
        #print(f"{int(self.model.predict(self.modelInput))}")
        mlMove = int(self.model.predict(tempList)[0]) # Get the models predicted move for the current state of the board
        # Now that I need to convert the models move back to a board position and return
        return self.convertToBoard(mlMove) 

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
                    if (self.turn == "O"): # If its O's turn instead of asking for input ask the model to predict
                        print(f"{self.turn}'s turn.")
                        print(f"The ml model is deciding where to place the O")
                        self.entryFormat = True
                        self.boardLocation = self.mlPredict()
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
                    self.boardLocation = self.boardLocation.split(",")
                    if (self.turn == "O"):
                        print(f"The model has chosen row #{int(self.boardLocation[0])}") 
                        print(f"\t  and column #{int(self.boardLocation[1])}")
                    else:
                        print(f"You have entered row #{int(self.boardLocation[0])}") 
                        print(f"\t  and column #{int(self.boardLocation[1])}")
                    self.entryValid = self.validateEntry(int(self.boardLocation[0]), int(self.boardLocation[1])) 
                self.board.gameBoard[int(self.boardLocation[0])][int(self.boardLocation[1])] = self.turn # Valid entry so add to board
                self.gameOver = self.checkEnd() # Determine if board is full or someone won or to continue the game
                self.switchPlayer() # Turn has been played and game is not over so switch turns
                self.entryValid = False # Prepare for a new input
            self.userInput = input("Another game? Enter Y or y for yes. \n")
        print("Thank you for playing!")
        
# This function reads in the tictac_single.txt and trains a model using KNN to predict the next optimal move for the O player
def trainModel():
    ticTacToeData = pd.read_csv("tictac_single.txt", delimiter=' ', header=None) # read the csv into dataframe
    #print(ticTacToeData.head())
    x = ticTacToeData.iloc[:, :9] # x0, x1, .. x8 is the board setup
    y = ticTacToeData.iloc[:, 9] # y is the index of the best move
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 42) # split 80/20 for training and testing, random_state so that its the same every time
    #print(x_train.shape, x_test.shape)

    # https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html
    model = KNeighborsClassifier()
    model.fit(x_train, y_train)

    """
    Here is where I need to optimize the model so im going to use all of the hyperparameters from the scikit learn website
    then do a gridsearchCV which is a slow process that tests all the combinations of parameters to see which gives the best model
    in this case based on accuracy. Leaf size default is 30 and n_neighbors default, im significantly reducing the amount of parameters I have
    because the runtime is way too long.
    """
    param_grid_knn = {
        'n_neighbors': [1, 3, 5, 79, 11],
        'weights': ['uniform', 'distance'],
        'algorithm': ['auto', 'brute'], # I am removing ball_tree and kd_tree since they do not seem to have an impact
        'leaf_size': [20, 30, 40],
         # Removing power parameter and metric because training is way too long with gridsearch
    }
    knn_grid = GridSearchCV(estimator = KNeighborsClassifier(),  # the model
                            param_grid = param_grid_knn,  # hyperparameter space
                             scoring='accuracy')  
    
    knn_grid.fit(x_train, y_train)
    model = knn_grid.best_estimator_
    # Confirming model was working 
    #print("KNN Best Parameters:", knn_grid.best_params_)
    #print("KNN Best Score:", knn_grid.best_score_)
    #print(f"Accuracy:", metrics.accuracy_score(y_test, y_predict))
    return model

def main():
    ticTacToe = Game()
    ticTacToe.playGame()
    

if __name__ == '__main__':
    main()
