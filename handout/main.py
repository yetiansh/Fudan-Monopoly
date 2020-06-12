from .classes import *
from .gui import guiShow


def main(parser):
    player = Player(parser)
    board = Board(initialLattices, initialPositions, player)
    app = guiShow(parser, board)
    return app
