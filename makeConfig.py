import pickle

config = {"initialLocation": 0,
          "initialMoney": 5,
          "initialSpirit": 0,
          "initialTime": 15,
          "initialKnowledge": 0,
          "windowSize": [1000, 600],
          "playerIconLocation": [0.0, 0.0],
          "playerIconSize": [0.2, 0.28],
          "gameMapSize": [0.8, 1.0],
          "gameMapLocation": [0.2, 0.0],
          "playerInfoSize": [15 / 1000, 6 / 600],
          "playerInfoLocation": [0.02, 0.3],
          "throwDiceSize": [20 / 1000, 1 / 600],
          "throwDiceLocation": [0.02, 0.5],
          "infoSize": [20 / 1000, 15 / 600],
          "infoLocation": [0.02, 0.55],
          "maxLines": 13,
          "playerSmallIconSize": [0.02, 0.028],
          "materialsPath": 'handout/materials/',
          "gameMap": 'gameMap.png',
          "nSteps": 5,
          "pauseTime": 0.1,
          }

player = {"playerName": 'fields',
          "playerIcon": 'handout/materials/playerIcon.png'}

pickle.dump(config, open('handout/materials/game.config', 'wb'))
pickle.dump(player, open('handout/materials/player.config', 'wb'))
