import alphaBetaPruning
import game

board=game.create()
game.whoIsFirst(board)
flag=True
while not game.isFinished(board):
    if game.isHumTurn(board):
        game.inputMove(board, flag)
    else:
        board=alphaBetaPruning.go(board)
    flag=False
game.printState(board)

