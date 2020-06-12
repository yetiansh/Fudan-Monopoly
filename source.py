import argparse

from handout import *

parser = argparse.ArgumentParser()

parser.add_argument('--gameName', type=str, default='Fudan Monopoly')

playerGroup = parser.add_argument_group('playerGroup')
playerGroup.add_argument('--playerName', type=str, default='fields')
playerGroup.add_argument('--playerIcon', type=str, default='playerIcon.png')
playerGroup.add_argument('--initialLocation', type=int, default=0)
playerGroup.add_argument('--initialMoney', type=int, default=20)
playerGroup.add_argument('--initialSpirit', type=int, default=5)
playerGroup.add_argument('--initialKnowledge', type=int, default=0)

displayGroup = parser.add_argument_group('displayGroup')
displayGroup.add_argument('--windowSize', type=int, default=[1000, 600])
displayGroup.add_argument('--playerIconSize', type=float, default=[0.2, 0.3])
displayGroup.add_argument('--playerIconLocation', type=float, default=[0.0, 0.0])
displayGroup.add_argument('--gameMapSize', type=float, default=[0.8, 1])
displayGroup.add_argument('--gameMapLocation', type=float, default=[0.2, 0.0])
displayGroup.add_argument('--playerInfoSize', type=float, default=[20 / 1000, 1 / 600])
displayGroup.add_argument('--playerInfoLocation', type=float, default=[[0.02, 0.31],
                                                                       [0.02, 0.36],
                                                                       [0.02, 0.41],
                                                                       [0.02, 0.46]])
displayGroup.add_argument('--throwDiceSize', type=float, default=[20 / 1000, 1 / 600])
displayGroup.add_argument('--throwDiceLocation', type=float, default=[0.02, 0.51])

materialsGroup = parser.add_argument_group('materialsGroup')
materialsGroup.add_argument('--materialsPath', type=str, default='handout/materials/')
materialsGroup.add_argument('--substrateMaterial', type=str, default='substrate.jpg')

parser = parser.parse_args()

if __name__ == '__main__':
    main(parser)
