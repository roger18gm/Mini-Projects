# 1. Name:
#      Roger Galan Manzano
# 2. Assignment Name:
#      Lab 01: Tic-Tac-Toe
# 3. Assignment Description:
#      Play the game of Tic-Tac-Toe
# 4. What was the hardest part? Be as specific as possible.
#      I struggled the most with determining the logic for ending the game 
#      by pressing 'q' or by there being a winner. I kept trying to hard-code
#      the input statements for player X and O when I should've been using a
#      variable. I found that I was copying and pasting code when I only needed
#      it in place. I also had difficulty opening a blank board at the start of 
#      a game when the previous one had been finished and was won. I found that
#      my logic in the read_board() function was setting the blank board to be 
#      the board that was in memory so it would never actually be finished. After
#      some debugging, I was able to fix this issue. 
# 5. How long did it take for you to complete the assignment?
#      6 hours

import json

# The characters used in the Tic-Tac-Too board.
# These are constants and therefore should never have to change.
X = 'X'
O = 'O'
BLANK = ' '

# A blank Tic-Tac-Toe board. We should not need to change this board;
# it is only used to reset the board to blank. This should be the format
# of the code in the JSON file.
blank_board = {  
            "board": [
                BLANK, BLANK, BLANK,
                BLANK, BLANK, BLANK,
                BLANK, BLANK, BLANK ]
        }

def read_board(filename):
    '''Read the previously existing board from the file if it exists.'''
    # Put file reading code here.
    with open(filename,"r") as file:
        jsonfile = json.load(file)
    # Setting file content to game board
    board = jsonfile
    return board


def save_board(filename, board):
    '''Save the current game to a file.'''
    # Put file writing code here.
    with open(filename,"w") as file:
        json.dump(board, file)


def display_board(board):
    '''Display a Tic-Tac-Toe board on the screen in a user-friendly way.'''
    # Put display code here.

    for i in range(9):
        print(f' {board[i]} ', end="")

        # print 3 board items on 3 separate lines
        if (i + 1) % 3 == 0:
            print()

            if i < 6:
                print("---+---+---")
        else: 
            print("|", end ="")


def is_x_turn(board):
    '''Determine whose turn it is by counting X's and O's on the board.'''
    x_count = board.count(X)
    o_count = board.count(O)
    # If the number of X's and O's is the same, it's X's turn.
    return x_count == o_count


def play_game(board):
    '''Play the game of Tic-Tac-Toe.'''
    playing = True

    while playing:
        display_board(board)

        # Determine whose turn it is
        if is_x_turn(board):
            player = X
        else:
            player = O

        # Gets input from the player
        while True:  # This loop ensures valid input for certain cases
            choice = input(f"{player}> ")

            # Allow the user to quit
            if choice == "q":
                save_board("game.json", board)  # Save the current game
                return False

            # Try to convert the input to an integer and check its range
            try:
                choice = int(choice)
                if choice < 1 or choice > 9:
                    print("Invalid input. Please enter a number between 1 and 9.")
                    continue
                if board[choice - 1] != BLANK:
                    print("That spot is already taken. Choose another one.")
                    continue
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 9.")
                continue  # Repeat the input prompt if it's not a valid number

            break

        # Update the board with the player's move
        board[choice - 1] = player

        # Check if the game is over
        if game_done(board, message=True):
            save_board("game.json", blank_board["board"])  # Reset the board in the file
            return False  # End the game loop



def game_done(board, message=False):
    '''Determine if the game is finished.
       Note that this function is provided as-is.
       You do not need to edit it in any way.
       If message == True, then we display a message to the user.
       Otherwise, no message is displayed. '''

    # Game is finished if someone has completed a row.
    for row in range(3):
        if board[row * 3] != BLANK and board[row * 3] == board[row * 3 + 1] == board[row * 3 + 2]:
            if message:
                print("The game was won by", board[row * 3])
            return True

    # Game is finished if someone has completed a column.
    for col in range(3):
        if board[col] != BLANK and board[col] == board[3 + col] == board[6 + col]:
            if message:
                print("The game was won by", board[col])
            return True

    # Game is finished if someone has a diagonal.
    if board[4] != BLANK and (board[0] == board[4] == board[8] or
                              board[2] == board[4] == board[6]):
        if message:
            print("The game was won by", board[4])
        return True

    # Game is finished if all the squares are filled.
    tie = True
    for square in board:
        if square == BLANK:
            tie = False
    if tie:
        if message:
            print("The game is a tie!")
        return True

    return False

# These user-instructions are provided and do not need to be changed.
print("Enter 'q' to suspend your game. Otherwise, enter a number from 1 to 9")
print("where the following numbers correspond to the locations on the grid:")
print(" 1 | 2 | 3 ")
print("---+---+---")
print(" 4 | 5 | 6 ")
print("---+---+---")
print(" 7 | 8 | 9 \n")
print("The current board is:")

# The file read code, game loop code, and file close code goes here.


try:
    # Opens game file if it exists; won't error out 
    board = read_board("game.json")

except FileNotFoundError:
    # New empty board for first game    
    board = blank_board["board"]

# Call to start the game
play_game(board)

