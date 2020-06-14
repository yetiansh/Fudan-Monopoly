import argparse
import pickle

from handout import *

parser = argparse.ArgumentParser()

parser.add_argument('--gameName', type=str, default='Fudan Monopoly')
parser.add_argument('--playerName', type=str, default='fields')
parser.add_argument('--playerIcon', type=str, default='playerIcon.png')
parser.add_argument('--configPath', type=str, default='handout/materials/game.config')
parser.add_argument('--gameContentsPath', type=str, default='handout/materials/gameContents.data')

parser = parser.parse_args()

config = pickle.load(open(parser.configPath, 'rb'))
for key in config.keys():
    exec('parser.' + key + ' = config[\'' + key + '\']')

contents = pickle.load(open(parser.gameContentsPath, 'rb'))
for key in contents.keys():
    exec('parser.' + key + ' = contents[\'' + key + '\']')

if __name__ == '__main__':
    main(parser)
