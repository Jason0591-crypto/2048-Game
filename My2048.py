# Import the needed modules
import random
import os
import timeit


# Create the board and the points
board = [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         ]
points = 0
# print(board)

# The move commands in the game
# W: up, S: down, A: left, D: right, E: exit game, R: restart
last_move = 'x'

# The statuses of the game
CONTINUE, WIN, LOSE = range(3)
status = CONTINUE
invalid = False


# The function that is used to make the program set everything to the start of a new game
def new_game():
    # This statement allows the board and the counter for the points to be accessed and modified in this
    # function.
    global board, status, last_move, points
    # The points and the board is set to 0
    board = [[0, 0, 0, 0],
             [0, 0, 0, 0],
             [0, 0, 0, 0],
             [0, 0, 0, 0]
             ]
    # Reset the points to zero
    points = 0
    # Clear all the empty spaces
    empty_space = list()
    # Reset the game status
    status = CONTINUE
    # Two nested for loops that repeatedly count the empty spaces of the game board (currently all of them)
    # and adds them to the list of empty spaces on the board.
    for i in range(4):
        for j in range(4):
            # Adds the space to the list of empty spaces on the board if it holds zero.
            if board[i][j] == 0:
                empty_space.append((i, j))
    # Determine the new spaces that will be filled with new numbers (a total of five).
    new_spaces = random.sample(empty_space, k=5)
    for new_space in new_spaces:
        # The new numbers that will be created on the board, which are chosen randomly.
        new_tile = random.choice([2, 2, 2, 2, 4])
        # Enter the random number into the chosen board space.
        board[new_space[0]][new_space[1]] = new_tile
    # Reset the last game move
    last_move = 'x'
    # Check if the numbers on the board could still be moved.
    check_moveable()


# A function that transposes the whole game board.
def transpose():
    # Allows the function to access the board and change it.
    global board
    # Create an empty board that will be the result of the transposing of the current board.
    new_board = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
                 ]
    for i in range(4):
        for j in range(4):
            new_board[i][j] = board[j][i]
    board = new_board


def vertical_flip():
    global board
    # Reverse the whole board, which acts as flipping the board vertically
    board = [*reversed(board)]


# This function is executed when the number blocks are going to be slided downwards, its goal is to
# determine whether the move was valid or not
def check_move_down():
    # These two loops will only check the top three rows, since the last row does not matter in the validity
    # of whether the blocks could be slided downwards.
    for j in range(4):
        for i in range(3):
            if board[i + 1][j] == board[i][j]:
                return True
            if board[i][j] > 0 and board[i + 1][j] == 0:
                return True
    return False


# This function will be executed after the last one was executed
# It moves all the number blocks on the board downwards
def move_down():
    # This statement globalizes status, allowing it to be used throughout the function
    global status, points
    for i in range(4):
        # The top index, which records down the movement or combining location of the target number block
        top_index = 3
        for j in range(2, -1, -1):
            # If the block is empty, then skip it
            if board[j][i] == 0:
                continue
            if board[top_index][i] == board[j][i]:
                points = points + board[top_index][j] * 2
                board[top_index][i] *= 2
                board[j][i] = 0
                top_index -= 1
                continue
            # If the top number block is empty, then move down
            if board[top_index][i] == 0:
                # Moving the number without updating the combining line pointer
                board[top_index][i] = board[j][i]
                # Clearing the former number block
                board[j][i] = 0
                continue
            # If the combining line is under the number block
            if top_index - 1 == j:
                top_index -= 1
                continue
            # The pointer moves up to the empty space
            top_index -= 1
            # Move to the empty space
            board[top_index][i] = board[j][i]
            # Clearing the former number block index
            board[j][i] = 0
            # Checking if
    for k in range(4):
        for l in range(4):
            if board[k][l] == 2048:
                status = WIN
                return True
    status = CONTINUE
    return False


def check_move_up():
    vertical_flip()
    result = check_move_down()
    vertical_flip()
    return result


def move_up():
    vertical_flip()
    result = move_down()
    vertical_flip()
    return result


def check_move_left():
    transpose()
    vertical_flip()
    result = check_move_down()
    vertical_flip()
    transpose()
    return result


def move_left():
    transpose()
    vertical_flip()
    result = move_down()
    vertical_flip()
    transpose()
    return result


def check_move_right():
    transpose()
    result = check_move_down()
    transpose()
    return result


def move_right():
    transpose()
    result = move_down()
    transpose()
    return result


# This function will create new number blocks on the board
def new_num():
    # The list of empty spaces on the board
    empty_space = list()
    # The numbers that could be put on the new block. Chosen randomly
    new_block = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 4])
    # The two loops here view each block one by one and determine if they are empty.
    # For each one of the blocks that is empty, the loops add its index on the board to a list.
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                empty_space.append((i, j))
    new_space = random.choice(empty_space)
    board[new_space[0]][new_space[1]] = new_block


continue_game_valid = {
    'up': True,
    'down': True,
    'left': True,
    'right': True
}


def check_moveable():
    global continue_game_valid, status, invalid
    continue_game_valid = {
        'up': check_move_up(),
        'down': check_move_down(),
        'left': check_move_left(),
        'right': check_move_right()
    }
    if len([1 for key in continue_game_valid if continue_game_valid[key]]):
        status = CONTINUE
    else:
        status = LOSE


def print_board():
    result = "|" + ("-" * 5 + "|") * 4 + "\n"
    for i in range(4):
        result += f"|{board[i][0]:^4} |{board[i][1]:^4} |{board[i][2]:^4} |{board[i][3]:^4} |\n"
    result += "|" + ("-" * 5 + "|") * 4 + "\n"
    print(result)


def exit_or_restart():
    # Start a new game if the player entered "r"(restart) as the next move
    if last_move == "r":
        new_game()
    # Exit the game if the player entered "e"(exit) as the next move
    elif last_move == "e":
        exit()


def last_input():
    global status
    # The initial output of this function
    output = f'last move: {last_move}'
    print(last_move)
    # Prints out a message to tell the player that they have lost the game
    if status == LOSE:
        print("You have lost this game, try again later")
        print("\nTotal Points:  ", points)
        input("Press <ENTER> to continue")
        exit_or_restart()
    # Prints out a message telling the move was invalid if the last move was an invalid one
    elif invalid:
        output += "\nInvalid move"
    # Prints out a message telling the player to continue the game if it is not finished
    elif status == CONTINUE:
        output += "\nContinue the game"
    # If the player have won the game, then print out a message that congrats them and tells them that they
    # have won.
    elif status == WIN:
        print("Congratulations, you won the game!")
        print("\nTotal Points:  ", points)
        exit_or_restart()
        # Prints out a message telling the player to continue the game if it is not finished
    else:
        output += "\nContinue the game"
        return output
    return output


# This function is the first of the two functions that will process the input moves the player entered.
# It
def input_screen():
    # This if-else statement decides whether
    if status == CONTINUE:
        # This line of code asks the player to enter the next command to execute
        return input("Please enter the next command: (w, s, a, d to move the blocks up, down, left, right; "
                     "e to exit the game, r to restart the game)")
    # If the game is over
    else:
        # This line of code asks the player to either restart the game or to exit the game
        return input("Please enter the next command: ('e' to exit the game, 'r' to restart the game)")


# print(input_screen())


# This function is the second of the two functions that will process the input moves the player entered.
# It
def input_valid(input_key):
    global last_move, invalid
    # If the game is over
    if status in (WIN, LOSE):
        if input_key in ("e", "r"):
            last_move = input_key
            invalid = False
            return True
    elif status == CONTINUE:
        last_move = input_key
        if input_key == "w":
            invalid = not continue_game_valid['up']
        elif input_key == "s":
            invalid = not continue_game_valid['down']
        elif input_key == "a":
            invalid = not continue_game_valid['left']
        elif input_key == "d":
            invalid = not continue_game_valid['right']
    else:
        last_move = input_key
        invalid = False
        return True


# Executes the moving commands of the board
def execute_move():
    if last_move == "w":
        move_up()
    elif last_move == "s":
        move_down()
    elif last_move == "a":
        move_left()
    elif last_move == "d":
        move_right()


# A function that clears the screen and then prints the current status of the game board, the last move,
# and the number blocks on it
def print_screen():
    # Clearing the screen
    os.system('cls')
    # Call the function print_board to print out the current status of the game board
    print(print_board())
    # Print the last move the player entered
    print(last_input())


def game():
    # Start a new game
    new_game()
    while True:
        # Prints the board and the number blocks on it
        print_board()
        #
        input_key = input_screen()
        #
        input_valid(input_key)
        #
        if invalid:
            continue
        #
        if last_move in ('e', 'r'):
            # Print the total points the player got in this round of the game
            print("Total points:    ", points)
            # Exit or restart the game, depending on the move the player entered
            exit_or_restart()
        else:
            # Move the number blocks on the board
            execute_move()
            print(last_input())
            # Create new number blocks
            new_num()
            # Check whether if the number blocks can still be moved
            check_moveable()


game()
