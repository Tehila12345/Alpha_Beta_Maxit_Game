# Tehila Reichman
# T.Z. 342737913
import copy

VIC = 10 ** 20  # The value of a winning board (for max)
LOSS = -VIC  # The value of a losing board (for max)
TIE = 0  # The value of a tie
SIZE = 4  # The length of the board
COMPUTER = 2  # Marks the computer's cells on the board
HUMAN = 1  # Marks the human's cells on the board
EMPTY_CELL = 1000  # Marks an empty cell on the board

'''
The state of the game is represented by a list of 6 items:
0. The game board - a matrix (list of lists) of ints. Empty cells = 1000 (which are printed as EMP),
1. Info about whether or not the game is over if if it's over who won
2. Who's turn is it: HUMAN or COMPUTER
3. the last cell picked
4. The human's current score
5. The computer's current score
'''
import random


def create():
    # Returns an empty board. The human plays first.
    board = []
    # creating a SIZE by SIZE board
    for i in range(SIZE):
        board = board + [SIZE * [0]]
    # putting random integers ranging from -15 to 15 in each cell in the board
    for i in range(SIZE):
        for j in range(SIZE):
            board[i][j] = random.randint(0, 30) - 15
    # return an array with the state of the board. The first element in the array is the board,
    # the second element is to know if the game is over and if so who won, the third element says who's turn it is now (the person's or the computer's),
    # the fourth element contains which cell was taken last turn, the fourth element contains the ammount of points that the human has and the fourth element contains the ammount of points that the computer has
    return [board, 1, HUMAN, [0, 0], 0, 0]


PREV_TURN = 3


def value(s):
    # Returns the heuristic value of s
    if isFinished(s):
        if s[5]>s[4]:
            return VIC
        elif s[5]<s[4]:
            return LOSS
        else:
            return TIE
    return s[5] - s[4]+0.0000001


def printState(s,first=False):
    # Prints the board. The empty cells are printed as 'EMP'
    # If the game is over it prints who won.
    # parameter first indicates whether it's currently the first turn
    for i in range(SIZE):
        for j in range(SIZE):
            if s[0][i][j] == EMPTY_CELL:
                print('EMP|', end='')
            else:
                print(s[0][i][j], end="")
                if s[0][i][j] >= 0:
                    print(" ", end='')
                if s[0][i][j] < 10 and s[0][i][j] > -10:
                    print(" ", end='')
                print("|", end='')
        print("\n", "__" * (2 * SIZE - 1))
    if first==False:
        print("last move was ", s[PREV_TURN])
        print("your score is ", s[4], " computer's score is ", s[5])
        if s[5] > s[4]:
            print("The computer has ", s[5] - s[4], " more points than you")
        elif s[5] < s[4]:
            print("You have ", s[4] - s[5], " more points than the computer")
        else:
            print("You and the computer both have the same amount of points")
    else:
        print("On your first turn you must pick a square on the first row")
    print("\n -- -- --\n")
    if s[1] == VIC:  # if the computer won
        print("Ha ha ha I won!")
    elif s[1] == LOSS:  # if the person won
        print("You did it!")
    elif s[1] == TIE:  # if there was a tie
        print("It's a TIE")


def isFinished(s):
    # Returns True if the game is over
    row, column = s[PREV_TURN]
    are_there_more_moves = False
    # If it's the human's turn then if there are any non empty cells in the row of the previous cell taken then there ARE more moves available to be taken
    if s[2] == HUMAN:
        for i in range(SIZE):
            if s[0][row][i] != EMPTY_CELL:
                are_there_more_moves = True
    # If it's the computer's turn then if there are any non empty cells in the column of the previous cell taken then there ARE more moves available to be taken
    else:
        for i in range(SIZE):
            if s[0][i][column] != EMPTY_CELL:
                are_there_more_moves = True
    # if there are no moves available to be taken then return True
    if not are_there_more_moves:
        return True


def isHumTurn(s):
    # Returns True if it's the human's turn
    return s[2] == HUMAN


def whoIsFirst(s):
    # The user decides who plays first
    input_user = "1"
    input_user = input("Who plays first? 1-me / anything else-you. : ")
    if input_user == "1":
        s[2] = COMPUTER
    else:
        s[2] = HUMAN


def makeMove(s, r, c):
    # Marks the cell chosen cell as empty
    # switches turns
    # Adds the number in the chosen cell to the score
    # Assumes the move is legal.
    # If there are no more available moves after this turn, marks s[1] according to who won
    if s[2] == COMPUTER:  # if it's the computer's turn add the number in the chosen cell to s[5] which contains the computer's score
        s[5] = s[5] + s[0][r][c]
    if s[2] == HUMAN:  # if it's the human's turn add the number in the chosen cell to s[4] which contains the human's score
        s[4] = s[4] + s[0][r][c]
    s[0][r][c] = EMPTY_CELL  # marks the board
    s[PREV_TURN] = (r, c)  # marks which cell was picked now
    s[2] = COMPUTER + HUMAN - s[2]  # switches turns
    if isFinished(s):  # If there are no possible moves left mark s[1] according to whoever won
        if s[5] - s[4] > 0:
            s[1] = VIC
        elif s[5] - s[4] < 0:
            s[1] = LOSS
        else:
            s[1] = TIE


def inputMove(s,first=False):
    # Reads, enforces legality and executes the user's move.
    # parameter first indicates whether it's currently the first turn, in which case the print function will print differently
    print(first)
    printState(s, first)
    flag = True
    while flag:
        move = int(input("Enter your next move: "))
        if move < 0 or move > SIZE - 1 or s[0][s[PREV_TURN][0]][move] == EMPTY_CELL:
            print("Ilegal move.")
        else:
            flag = False
            makeMove(s, s[PREV_TURN][0], move)


def getNext(s):
    # returns a list of the next states of s
    if s[2] == COMPUTER:
        ns = []
        column = s[PREV_TURN][1]  # getting the column which the next turn has to be in
        for r in range(SIZE):  # putting all the possible next states in ns
            if s[0][r][column] != EMPTY_CELL:
                tmp = copy.deepcopy(s)
                makeMove(tmp, r, column)
                ns.append(tmp)
        ns.sort(key=value,
                reverse=True)  # sorting the states in ns in reverse order according to their values to make the program more efficient
    else:
        ns = []
        row = s[PREV_TURN][0]  # getting the row which the next turn has to be in
        for c in range(SIZE):  # putting all the possible next states in ns
            if s[0][row][c] != EMPTY_CELL:
                tmp = copy.deepcopy(s)
                makeMove(tmp, row, c)
                ns.append(tmp)
        ns.sort(key=value)  # sorting the states in ns according to their values to make the program more efficient
    return ns
