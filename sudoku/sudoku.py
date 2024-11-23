# 1. Name:
#      Roger Galan Manzano
# 2. Assignment Name:
#      Lab 05 : Sudoku Draft
# 3. Assignment Description:
#      Allow a user to play a basic version of a Sudoku game
# 4. What was the hardest part? Be as specific as possible.
#      This week I had the greatest challenge with updating my convert_move function 
#      so that user coordinate location could be flexible and interpreted correctly 
#      without order mattering.
# 5. How long did it take for you to complete the assignment?
#      5 hours

import json


def main():
    '''Gameplay begins and continues until user types 'Q' '''
    board = load_board()

    while True:
        # Shows gameboard
        display_board(board) 
        if play_round(board) == False: 
            # Once finished, save and quit
            filename = input("Where would you like to save your board? ")
            save_board(board, filename)
            return False


def play_round(board):
    '''Parameter: List of lists 'board'
        Begins a new round where the user is prompted to enter a board
        location in a similar fashion to 'a1' and afterward is prompted to
        enter a value from 1-9. If valid inputs are entered, those arguments
        will be passed into the convert_move() and is_move_valid() functions.
        Returns: list of lists 'board'   '''
    
    while True:
        try:
            print("Specify a coordinate to edit or 'Q' to save and quit:")
            str_coord = input("> ")

            if str_coord == "Q": 
                # Exit loop and save
                return False 
            if len(str_coord) != 2: 
                # Error message if receives unexpected value
                print("Invalid coordinate format. Please enter a valid coordinate in the form of 'a1', 'A1', '1a', or '1A'")
                continue
           
            try:
                # Call convert_move to parse from string to integer list
                int_coords = convert_move(str_coord) 
                if int_coords is None:
                    print("Invalid coordinate format. Please enter a valid coordinate in the form of 'a1', 'A1', '1a', or '1A'")
                    continue
            except ValueError as ve:
                print(ve, "Invalid coordinate input.")
            except Exception as e:
                print(e)
                continue
            
            try:
                # Ensure move value is in the correct range
                move = int(input(f"What number goes in {str_coord}? "))
                if move < 1 or move > 9:
                    print("Please enter a number between 1 and 9.")
                    continue
            except ValueError as e:
                print(e, "Please enter a number between 1 and 9.")
                continue

            try:
                if is_move_valid(board,move,int_coords) == True: 
                    # If move is valid, update the move on the board
                    board[int_coords[1]][int_coords[0]] = move
                    return board
                else:
                    print("Invalid move. Position already filled or out of bounds.")
                    continue
            except TypeError as e:
                print(e)


        except Exception as e:
            print("Unexpected error: ", e)

def load_board():
    '''Parameter: None
        Desc: Retrieves board based on if the filename
        exists within the same directory
        Return: list of lists named board '''
    
    while True:
        try:       
            # Default boards    
            print("Easy board: 131.05.Easy.json")     
            print("Medium board: 131.05.Medium.json")  
            print("Hard board: 131.05.Hard.json")
            board_name = input("Where is your board located? ")

            with open(board_name,"r") as file:
                board = json.load(file)
                break
        except FileNotFoundError as err:
            print(err,"Please enter a valid filename or play with one of the boards above.")
    
    return board["board"]


def display_board(board):
    '''Parameter: board, list of lists
        Desc: Iterates through each row and column and puts
        the values from the board to the console
        Return: None'''

    print("   A B C D E F G H I")
    for row in range(9):
        if row == 3 or row == 6:
            print ("   -----+-----+-----")
            print(f"{row+1}  ",end="")
        else:
            print(f"{row+1}  ",end="")

        for col in range(9):
            separator = [" "," ","|"," "," ","|"," "," ","\n"]
            
            if board[row][col] == 0:
                print(" ",end="")
            else:
                print(board[row][col], end="")
            print(separator[col],end="")


def save_board(board, filename):
    '''Parameters: board, list of lists and filename, string
        Desc: Function writes the board to a file named by the user.
        Return: None '''
    
    board_file = {"board": board}
    with open(filename,"w") as file:
        json.dump(board_file, file)


def convert_move(str_coord):
    '''Parameter: A 2-character string
        Desc: Splits the string into two parts and computes the
        numerical value for the column coordinate and row coordinate. 
        Parses these values into integers and adds to new list
        Return: list with two values'''

    if not isinstance(str_coord, str) or len(str_coord) != 2:
        raise ValueError("Input must be a two-character string.")
    
    first_char = str_coord[0].lower()
    second_char = str_coord[1].lower()
    int_coords = []

    try: # Assign coordinate values based on what type of character comes first
        if first_char.isdigit(): # '1'
            row_coord = int(first_char) - 1
            # assert that column coordinate is less than 'I'
            if ord(second_char) > ord('i'):
                raise ValueError("Letter character should be between A and I.")
            # Get numerical coordinate value from ordenal subtraction
            col_coord = ord(first_char) - ord('a')
            if not second_char.isalpha():
                raise ValueError("Second character must be a letter if the first is a number. (Ex: 1a, 1A)")
            col_coord = ord(second_char) - ord('a')

            

        elif first_char.isalpha(): # 'a'
            # assert that column coordinate is less than 'I'
            if ord(first_char) > ord('i'):
                raise ValueError("Letter character should be between A and I.")
            # Get numerical coordinate value from ordenal subtraction
            col_coord = ord(first_char) - ord('a')
            if not second_char.isdigit():
                raise ValueError("Second character must be a number if the first is a letter. (Ex: a1, A1)")
            row_coord = int(second_char) - 1

        else:
            raise ValueError("Characters must be an alphabetical letter or number")


    except ValueError as val_err:
        (f"Invalid coordinate: {val_err}")
        return

    int_coords = [col_coord, row_coord]
    assert len(int_coords) == 2
    return int_coords


def is_move_valid(board,move,int_coords):
    '''Parameter: List of lists for game board, integer move,
        and the integer coordinates to place the move
        Desc: Iterates through the desired row and column to 
        determine if it already contains the move value. Also
        iterates through the square of the coordinates to see
        if the move value is present.
        Return: False if move is already present, True if it isn't'''
    
    col_coord = int_coords[0]
    row_coord = int_coords[1]

    if board[col_coord][row_coord] != 0: # Check desired location for a number already present
        print("Selected square is already filled with a number.")
        return False
    
    for col in range(9): # Check all values in column to see if move is present
        if board[col][col_coord] == move:
            print("Number already exists within the column.")
            return False
        
    for row in range(9): # Check all values in row to see if move is present
        if board[row_coord][row] == move:
            print("Number already exists within the row.")
            return False

    col_start = col_coord // 3 * 3
    row_start = row_coord // 3 * 3
    # Check all values in 3x3 square to see if move is present
    for col in range(col_start, col_start+3):
        for row in range(row_start, row_start+3):
            if board[row][col] == move:
                print("Number already exists within the square.")
                return False
    return True
         

if __name__ == "__main__":
    main()