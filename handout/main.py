import pickle

from .classes import *
from .games import *
from .gui import *


def main(parser, board):
    player = Player(parser)
    board = Board(lattices, positions, player)
    guiShow(board, firstDisplay=True)
    while board.player.location < len(positions):
        guiThrowDice(board)

        pass