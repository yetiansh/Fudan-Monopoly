import argparse
import pickle

from handout import *

parser = argparse.ArgumentParser()

parser.add_argument('--gameName', type=str, default='Fudan Monopoly')
parser.add_argument('--playerName', type=str, default=None)
parser.add_argument('--playerIcon', type=str, default=None)
parser.add_argument('--playerConfigPath', type=str, default='handout/materials/player.config')
parser.add_argument('--gameConfigPath', type=str, default='handout/materials/game.config')
parser.add_argument('--gameContentsPath', type=str, default='handout/materials/gameContents.dat')

parser = parser.parse_args()

if parser.playerName is None or parser.playerIcon is None:
    playerConfig = pickle.load(open(parser.playerConfigPath, 'rb'))
    if parser.playerName is None:
        parser.playerName = playerConfig['playerName']
    if parser.playerIcon is None:
        parser.playerIcon = playerConfig['playerIcon']

gameConfig = pickle.load(open(parser.gameConfigPath, 'rb'))
for key in gameConfig.keys():
    exec('parser.' + key + ' = gameConfig[\'' + key + '\']')

gameContents = pickle.load(open(parser.gameContentsPath, 'rb'))
for key in gameContents.keys():
    exec('parser.' + key + ' = gameContents[\'' + key + '\']')

if __name__ == '__main__':
    main(parser)
