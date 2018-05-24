""" gametree.py

Contains the definition of the GameTree class.
This file forms part of the assessment for CP2410 Assignment 2

************** Kye Cook ****************************

"""
from connect3board import Connect3Board


class GameTree:
    MAX_PLAYER = 'O'
    MIN_PLAYER = '#'
    MAX_WIN_SCORE = 1
    MIN_WIN_SCORE = -1
    DRAW_SCORE = 0

    def __init__(self, root_board):
        self._root = GameTree._Node(root_board)

    # noinspection PyProtectedMember
    class _Node:
        __slots__ = '_gameboard', '_children', '_score'

        def __init__(self, gameboard: Connect3Board):
            self._gameboard = gameboard
            self._children = []
            self._create_children()
            self._score = self._compute_score()

        def _create_children(self):
            game = self._gameboard
            win = game.get_winner()
            if win is None:
                for i in range(0,3):
                    board = self._gameboard.make_copy()
                    if board.can_add_token_to_column(i):
                        board = self._gameboard.make_copy()
                        board.add_token(i)
                        self._children.append(GameTree._Node(board))
                    else:
                        self._children.append(None)

        def _compute_score(self):
            win = self._gameboard.get_winner()
            if win == GameTree.MAX_PLAYER:
                return GameTree.MAX_WIN_SCORE
            elif win == GameTree.MIN_PLAYER:
                return GameTree.MIN_WIN_SCORE
            elif win == 'DRAW':
                return GameTree.DRAW_SCORE
            else:
                score = 0
                for child in self._children:
                    if child is not None:
                        score += child._score
                return score
