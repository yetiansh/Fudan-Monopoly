import pickle
import time
import tkinter as tk
from PIL import ImageTk, Image

from .classes import *


class App:
    def __init__(self, parser, board):
        self.parser = parser
        self.lap = 0

        self.board = board
        self.window = tk.Tk()
        self.window.title(parser.gameName)
        self.window.geometry(str(parser.windowSize[0]) + 'x' + str(parser.windowSize[1]))
        self.window.resizable(width=False, height=False)

        self.playerImage = Image.open(parser.materialsPath + parser.playerIcon)
        self.playerImage = self.playerImage.resize((int(parser.playerIconSize[0] * parser.windowSize[0]),
                                                    int(parser.playerIconSize[1] * parser.windowSize[1])),
                                                   Image.ANTIALIAS)
        self.playerIcon = ImageTk.PhotoImage(self.playerImage)
        self.playerButton = tk.Button(self.window, image=self.playerIcon, relief=tk.FLAT,
                                      width=int(parser.playerIconSize[0] * parser.windowSize[0]),
                                      height=int(parser.playerIconSize[1] * parser.windowSize[1]),
                                      command=lambda: board.player(self.parser))
        self.playerButton.place(x=int(parser.playerIconLocation[0] * parser.windowSize[0]),
                                y=int(parser.playerIconLocation[1] * parser.windowSize[1]))

        self.gameMapImage = Image.open(parser.materialsPath + parser.substrateMaterial)
        self.gameMapImage = self.gameMapImage.resize((int(parser.gameMapSize[0] * parser.windowSize[0]),
                                                      int(parser.gameMapSize[1] * parser.windowSize[1])),
                                                     Image.ANTIALIAS)
        self.gameMapIcon = ImageTk.PhotoImage(self.gameMapImage)
        self.gameMapLabel = tk.Label(self.window, image=self.gameMapIcon,
                                     width=int(parser.gameMapSize[0] * parser.windowSize[0]),
                                     height=int(parser.gameMapSize[1] * parser.windowSize[1]))
        self.gameMapLabel.place(x=int(parser.gameMapLocation[0] * parser.windowSize[0]),
                                y=int(parser.gameMapLocation[1] * parser.windowSize[1]))

        self.playerInfoLabel = tk.Label(self.window, text='Name: ' + str(board.player.name) + '\n' +
                                                          'Grade: ' + str(board.player.grade) + '\n' +
                                                          'Money: ' + str(board.player.money) + '\n' +
                                                          'Time: ' + str(board.player.time) + '\n' +
                                                          'Spirit: ' + str(board.player.spirit),
                                        justify=tk.LEFT, padx=0, pady=0,
                                        width=int(parser.playerInfoSize[0] * parser.windowSize[0]),
                                        height=int(parser.playerInfoSize[1] * parser.windowSize[1]))
        self.playerInfoLabel.place(x=int(parser.playerInfoLocation[0] * parser.windowSize[0]),
                                   y=int(parser.playerInfoLocation[1] * parser.windowSize[1]))

        self.throwDiceButton = tk.Button(self.window, text='Throw dice', command=lambda: App.main(self),
                                         width=int(parser.throwDiceSize[0] * parser.windowSize[0]),
                                         height=int(parser.throwDiceSize[1] * parser.windowSize[1]))
        self.throwDiceButton.place(x=int(parser.throwDiceLocation[0] * parser.windowSize[0]),
                                   y=int(parser.throwDiceLocation[1] * parser.windowSize[1]))

        self.infoLabel = tk.Label(self.window, text='Welcome to\nFudan Monopoly!', justify=tk.LEFT,
                                  width=int(parser.infoSize[0] * parser.windowSize[0]),
                                  height=int(parser.infoSize[1] * parser.windowSize[1]))
        self.infoLabel.place(x=int(parser.infoLocation[0] * parser.windowSize[0]),
                             y=int(parser.infoLocation[1] * parser.windowSize[1]))

        #   需要在这里放下所有的地点和卡片
        self.playerSmallImage = self.playerImage.resize((int(parser.playerIconSize[0] * parser.windowSize[0]),
                                                         int(parser.playerIconSize[1] * parser.windowSize[1])),
                                                        Image.ANTIALIAS)
        self.playerSmallIcon = ImageTk.PhotoImage(self.playerSmallImage)
        self.playerSmallLabel = tk.Label(self.window, image=self.playerSmallIcon,
                                         width=int(parser.playerSmallIconSize[0] * parser.windowSize[0]),
                                         height=int(parser.playerSmallIconSize[1] * parser.windowSize[1]))
        self.playerSmallLabel.place(x=int(initialPositions[self.board.player.location][0] *
                                          self.gameMapLabel['width']) + self.gameMapLabel.place_info()['x'],
                                    y=int(initialPositions[self.board.player.location][1] *
                                          self.gameMapLabel['height']) + self.gameMapLabel.place_info()['y'])
        self.window.mainloop()

    def main(self):
        dice = self.throwDice()

        if self.board.player.location + dice > len(self.board.positions):
            self.lap = self.lap + 1

        if self.lap in [0, 1]:
            self.board.player.location = self.board.player.location + dice % len(self.board.positions)
        elif self.lap == 2:
            self.board.player.location = self.board.player.location + dice % len(self.board.positions)
            self.showFinalExam()
        elif self.lap == 3:
            self.enterNextGrade()

        self.movePlayer()
        lattice = self.board.lattices[self.board.player.location]
        if isinstance(lattice, Chance):
            pass
        elif isinstance(lattice, Site):
            pass
        elif not isinstance(lattice, BlankLattice):
            raise RuntimeError('Invalid Lattice!')

    def movePlayer(self):
        self.playerSmallLabel.place(x=int(self.board.positions[self.board.player.location][0] *
                                          self.gameMapLabel['width']) + self.gameMapLabel.place_info()['x'],
                                    y=int(self.board.positions[self.board.player.location][1] *
                                          self.gameMapLabel['height']) + self.gameMapLabel.place_info()['y'])

    def updateMap(self):
        pass

    def updatePlayerInfo(self):
        self.playerInfoLabel['text'] = 'Name: ' + str(self.board.player.name) + '\n' +\
                                       'Grade: ' + str(self.board.player.grade) + '\n' +\
                                       'Money: ' + str(self.board.player.money) + '\n' +\
                                       'Time: ' + str(self.board.player.time) + '\n' +\
                                       'Spirit: ' + str(self.board.player.time)

    def showFinalExam(self):
        self.board = Board(latticesWithFinalExam, positionsWithFinalExam, self.board.player)
        self.updateMap()

    def enterNextGrade(self):
        def endOfGame():
            endWindow = tk.Tk()
            endWindow.geometry('200x300')

        index = grades.index(self.board.player.grade)
        if index == len(grades) - 1:
            endOfGame()
        else:
            self.board.player.grade = grades[index + 1]
            self.board = Board(initialLattices, initialPositions, self.board.player)
            self.updatePlayerInfo()
            self.updateMap()
            self.lap = 0

    def throwDice(self):
        dice = random.randint(1, 6)
        self.infoLabel['text'] = self.truncateText(self.infoLabel['text'] + '\nResult is ' + str(dice))
        return dice

    def truncateText(self, text):
        n = text.count('\n') + 1
        if n <= self.parser.maxLines:
            return text
        else:
            index = 0
            for i in range(n - self.parser.maxLines):
                index = index + text[index + 1:].index('\n')
            return text[index + 1:]

    def drawCard(self, remainedCards=None):
        if remainedCards is None:
            remainedCards = remainedChances
        if len(remainedCards) is 0:
            remainedCards = chances

        card = random.sample(remainedCards, 1)
        self.board.player.record.append(card)
        remainedChances.remove(card)
        return card

def guiShow(parser, board):
    app = App(parser, board)
    return app

