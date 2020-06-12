import pickle

from .classes import *
from .games import *
from .gui import *


def main(parser):
    player = Player(parser)
    board = Board(lattices, positions, player)
    substrate = guiShow(parser, board)
    # while board.player.location < len(positions):
    #     guiThrowDice(board)
    #
    #     pass