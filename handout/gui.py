import tkinter as tk
from PIL import ImageTk, Image

from .classes import *


class Substrate:
    def __init__(self, parser, board):
        self.parser = parser
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

        self.playerNameLabel = tk.Label(self.window, text='name: ' + str(board.player.name),
                                        width=int(parser.playerInfoSize[0] * parser.windowSize[0]),
                                        height=int(parser.playerInfoSize[1] * parser.windowSize[1]))
        self.playerNameLabel.place(x=int(parser.playerInfoLocation[0][0] * parser.windowSize[0]),
                                   y=int(parser.playerInfoLocation[0][1] * parser.windowSize[1]))

        self.playerGradeLabel = tk.Label(self.window, text='grade: ' + str(board.player.grade),
                                         width=int(parser.playerInfoSize[0] * parser.windowSize[0]),
                                         height=int(parser.playerInfoSize[1] * parser.windowSize[1]))
        self.playerGradeLabel.place(x=int(parser.playerInfoLocation[1][0] * parser.windowSize[0]),
                                    y=int(parser.playerInfoLocation[1][1] * parser.windowSize[1]))

        self.playerMoneyLabel = tk.Label(self.window, text='money: ' + str(board.player.money),
                                         width=int(parser.playerInfoSize[0] * parser.windowSize[0]),
                                         height=int(parser.playerInfoSize[1] * parser.windowSize[1]))
        self.playerMoneyLabel.place(x=int(parser.playerInfoLocation[2][0] * parser.windowSize[0]),
                                    y=int(parser.playerInfoLocation[2][1] * parser.windowSize[1]))

        self.playerSpiritLabel = tk.Label(self.window, text='spirit: ' + str(board.player.spirit),
                                          width=int(parser.playerInfoSize[0] * parser.windowSize[0]),
                                          height=int(parser.playerInfoSize[1] * parser.windowSize[1]))
        self.playerSpiritLabel.place(x=int(parser.playerInfoLocation[3][0] * parser.windowSize[0]),
                                     y=int(parser.playerInfoLocation[3][1] * parser.windowSize[1]))

        self.throwDiceButton = tk.Button(self.window, text='throw dice', command=guiThrowDice,
                                         width=int(parser.throwDiceSize[0] * parser.windowSize[0]),
                                         height=int(parser.throwDiceSize[1] * parser.windowSize[1]))
        self.throwDiceButton.place(x=int(parser.throwDiceLocation[0] * parser.windowSize[0]),
                                   y=int(parser.throwDiceLocation[1] * parser.windowSize[1]))

        self.window.mainloop()


def guiShow(parser, board, substrate=None):
    #   firstDisplay为False时在原来显示的基础上更改显示
    #   firstDisplay为True时重新进行显示
    #   待完成
    if substrate is None:
        substrate = Substrate(parser, board)
    else:
        pass

    return substrate


def guiThrowDice():
    #   丢筛子，调用throwDice
    #   待完成
    def throwDice(top):
        result = random.randint(1, 6)
        dice = tk.Label(top, text='Results is: ' + str(result))
        dice.pack(side='top')

        return random.randint(1, 6)

    newWindow = tk.Tk()
    newWindow.title('Throw Dice')
    newWindow.geometry('200x60')
    text = tk.Button(newWindow, text='Throw Dice', command=lambda: throwDice(newWindow))
    text.pack(side='bottom')
    newWindow.mainloop()

#   还有一些其他动作
#   待完成
