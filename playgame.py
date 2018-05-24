""" playgame.py

Contains the Connect 3 game playing application.
This file forms part of the assessment for CP2410 Assignment 2

************** Kye Cook ****************************

"""
from connect3board import Connect3Board
from gametree import GameTree


def main():
    test = Connect3Board(3, 3)
    Tree = GameTree(test)
    print('Welcome to Connect 3 by Kevin Richards')
    mode = get_mode()
    while mode != 'Q':
        if mode == 'A':
            run_two_player_mode()
        elif mode == 'B':
            run_ai_mode(Tree)
        mode = get_mode()


def run_two_player_mode():
    row = checkIntValue(0)
    column = checkIntValue(1)
    board = Connect3Board(row,column)
    print(board)
    for i in range(0,4):
        board.move()
    winner = board.get_winner()
    while winner is None:
        board.move()
        winner = board.get_winner()
    print("Player " + winner + " wins!")
    pass


def run_ai_mode(Tree):
    Tree = Tree._root
    char = input("Will you play as O or #? ")
    while char not in "#O":
        char = input("Will you play as O or #? ")

    board = Connect3Board(3,3)
    print(board)
    if char == 'O':
        winner = None
        while winner is None:
            mover = board.check_player_move(1)
            board.add_token(mover)
            print(board)
            winner = board.get_winner()
            if winner is not None:
                break
            print("AI's turn")
            Tree = Tree._children[mover]
            list = Tree._children
            scores = []
            for child in list:
                if child is not None:
                    scores.append(child._score)
                else:
                    scores.append(1000)
            min_score = min(scores)
            column_no = 0
            for child_score in scores:
                if child_score == min_score or child_score==-1:
                    board.add_token(column_no)
                    Tree = Tree._children[column_no]
                    break
                column_no+=1

            print(board)
            winner = board.get_winner()
            if winner is not None:
                break
        print("Player " + winner + " wins!")

    else:

        winner = None
        while winner is None:
            print("AI's turn")
            list = Tree._children
            scores = []
            for child_score in list:
                if child_score is not None:
                    scores.append(child_score._score)
                else:
                    scores.append(-1000)
            max_score = max(scores)
            column_no = 0
            for child_score in scores:
                if child_score == max_score or child_score==1:
                    board.add_token(column_no)
                    Tree = Tree._children[column_no]
                    break
                column_no += 1
            print(board)
            winner = board.get_winner()
            if winner is not None:
                break
            mover = board.check_player_move(1)
            board.add_token(mover)
            print(board)
            Tree = Tree._children[mover]
            winner = board.get_winner()
            if winner is not None:
                break
        print("Player " + winner + " wins!")


def get_mode():
    mode = input("A. Two-player mode\nB. Play against AI\nQ. Quit\n>>> ")
    while mode[0].upper() not in 'ABQ':
        mode = input("A. Two-player mode\nB. Play against AI\nQ. Quit\n>>> ")
    return mode[0].upper()


def get_int(prompt):
    result = 0
    finished = False
    while not finished:
        try:
            result = int(input(prompt))
            finished = True
        except ValueError:
            print("Please enter a valid integer.")
    return result


def checkIntValue(d):
    while True:
        try:
            if d == 0:
                row = int(input("How many rows? (3 to 7) "))
            else:
                row = int(input("How many columns? (3 to 7) "))
        except ValueError:
            continue
        else:
            if row < 3 or row > 7:
                continue
            else:
                return (row)


if __name__ == '__main__':
    main()
