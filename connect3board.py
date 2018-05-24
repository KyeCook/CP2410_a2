""" connect3board.py

Contains the definition of the Connect3Board class.
This file forms part of the assessment for CP2410 Assignment 2

************** Kye Cook ****************************

"""

import copy


class Connect3Board:
    TOKENS = ['O', '#']
    DRAW = 'DRAW'

    __slots__ = '_rows', '_cols', '_board', '_turn_number'

    def __init__(self, rows, cols, turn_number=0, board=None):
        self._rows = rows
        self._cols = cols
        self._board = board
        self._turn_number = turn_number
        if board is None:
            self._make_board()

    def get_columns(self):
        """ Returns the number of columns in the board """
        return self._cols

    def get_rows(self):
        """ Returns the number of rows in the board """
        return self._rows

    def get_turn_number(self):
        """ Returns the turn number, starting at 0 """
        return self._turn_number

    def get_whose_turn(self):
        """ Returns the token (O or #) of the player whose turn it is currently"""
        return Connect3Board.TOKENS[self._turn_number % 2]

    def get_winner(self):
        """ Returns None if the game is not complete, DRAW if no more moves can be played and there is no winner,
        or the token (O or #) that has won the game by making three-in-a-row horizontally, vertically, or diagonally."""
        # this only works correctly for 3*3, you will need to implement a solution that works for larger
        # sized boards
        for r in range(0,self._rows-2):
            for c in range(0,self._cols-2):
                if self._board[r][c] is not None and \
                        (self._board[r][c] == self._board[r][c + 1] == self._board[r][c + 2] or
                         self._board[r][c] == self._board[r + 1][c] == self._board[r + 2][c] or
                         self._board[r][c] == self._board[r + 1][c + 1] == self._board[r + 2][c + 2]):
                    return self._board[r][c]
                elif self._board[r + 1][c] is not None and self._board[r + 1][c] == self._board[r + 1][c + 1] == \
                        self._board[r + 1][c + 2]:
                    return self._board[r + 1][c]
                elif self._board[r + 2][c] is not None and \
                        (self._board[r + 2][c] == self._board[r + 2][c + 1] == self._board[r + 2][c + 2] or
                         self._board[r + 2][c] == self._board[r + 1][c + 1] == self._board[r][c + 2]):
                    return self._board[r + 2][c]
                elif self._board[r][c + 1] is not None and self._board[r][c + 1] == self._board[r + 1][c + 1] == \
                        self._board[r + 2][c + 1]:
                    return self._board[r][c + 1]
                elif self._board[r][c + 2] is not None and self._board[r][c + 2] == self._board[r + 1][c + 2] == \
                        self._board[r + 2][c + 2]:
                    return self._board[r][c + 2]

        # no winner discovered, so check for draw or otherwise return None
        if self._turn_number >= self._rows * self._cols:
            return Connect3Board.DRAW
        else:
            return None

    def add_token(self, column):
        """ Adds the token of the current player to the board at the indicated column and advances
        the game by one turn. Returns True if successful, False if the turn is not made."""
        assert 0 <= column < self._cols
        token = Connect3Board.TOKENS[self._turn_number % 2]
        if self._board[0][column] is None:
            for row in range(self._rows - 1, -1, -1):
                if self._board[row][column] is None:
                    self._board[row][column] = token
                    self._turn_number += 1
                    return True
        return False

    def can_add_token_to_column(self, column):
        """ Returns true if and only it is possible to add a token to the given column """
        return 0 <= column < self._cols and self._board[0][column] is None

    def make_copy(self):
        """ Returns a copy of the board, at the same turn number, and with the same contents """
        return Connect3Board(self._rows, self._cols, self._turn_number, copy.deepcopy(self._board))

    def __str__(self):
        column_labels = ' ' + ''.join(str(i) for i in range(self._cols))
        rows = [column_labels]
        for row in self._board:
            rows.append('|' + ''.join(c if c is not None else ' ' for c in row) + '|')
        rows.append('-' * (self._cols + 2))
        rows.append(column_labels)
        return '\n'.join(rows)

    def _make_board(self):
        self._board = []
        for i in range(self._rows):
            self._board.append([None] * self._cols)

    def move(self):
        mover = self.check_player_move()
        self.add_token(mover)
        print(self)
        return mover

    def check3x3(self, x, y):
        if self._board[x][y] is not None and \
                (self._board[x][y] == self._board[x][y + 1] == self._board[x][y + 2] or
                 self._board[x][y] == self._board[x + 1][y] == self._board[x + 2][y] or
                 self._board[x][y] == self._board[x + 1][y + 1] == self._board[x + 2][y + 2]):
            return self._board[x][y]
        elif self._board[x + 1][y] is not None and self._board[x + 1][y] == self._board[x + 1][y + 1] == \
                self._board[x + 1][y + 2]:
            return self._board[x + 1][y]
        elif self._board[x + 2][y] is not None and \
                (self._board[x + 2][y] == self._board[x + 2][y + 1] == self._board[x + 2][y + 2] or
                 self._board[x + 2][y] == self._board[x + 1][y + 1] == self._board[x][y + 2]):
            return self._board[x + 2][y]
        elif self._board[x][y + 1] is not None and self._board[x][y + 1] == self._board[x + 1][y + 1] == \
                self._board[x + 2][y + 1]:
            return self._board[x][y + 1]
        elif self._board[x][y + 2] is not None and self._board[x][y + 2] == self._board[x + 1][y + 2] == \
                self._board[x + 2][y + 2]:
            return self._board[x][y + 2]
        else:
            return None

    def check_player_move(self, ai = 0):
        two_player_move = "Player " + self.get_whose_turn() + "'s turn. Choose column (0 to " + str(self._cols) + "): "
        ai_move = "Your turn. Choose column (0 to 2): "
        if ai == 1:
            string = ai_move
        else:
            string = two_player_move
        while True:
            try:
                move = int(input(string))
            except ValueError:
                continue
            else:
                if move < 0 or move >= self._cols:
                    continue
                else:
                    return (move)
