import os
import time
import pickle

from PIL import ImageTk, Image
from tkinter import filedialog

from .classes import *


class App:
    def __init__(self, parser):
        self.parser = parser
        self.player = Player(parser)
        self.lattices = parser.initialLattices
        self.sizes = parser.initialSizes
        self.locations = parser.initialLocations
        self.lap = 0

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
                                      command=self.showPlayerInfo())
        self.playerButton.place(x=int(parser.playerIconLocation[0] * parser.windowSize[0]),
                                y=int(parser.playerIconLocation[1] * parser.windowSize[1]))

        self.gameMapImage = Image.open(parser.materialsPath + parser.gameMap)
        self.gameMapImage = self.gameMapImage.resize((int(parser.gameMapSize[0] * parser.windowSize[0]),
                                                      int(parser.gameMapSize[1] * parser.windowSize[1])),
                                                     Image.ANTIALIAS)
        self.gameMapIcon = ImageTk.PhotoImage(self.gameMapImage)
        self.gameMapLabel = tk.Label(self.window, image=self.gameMapIcon)
        self.gameMapLabel.place(x=int(parser.gameMapLocation[0] * parser.windowSize[0]),
                                y=int(parser.gameMapLocation[1] * parser.windowSize[1]))

        self.playerInfoLabel = tk.Label(self.window, text='姓名: ' + str(self.player.name) + '\n' +
                                                          '年级: ' + str(self.player.grade) + '\n' +
                                                          '金钱: ' + str(self.player.money) + '\n' +
                                                          '时间: ' + str(self.player.time) + '\n' +
                                                          '体力: ' + str(self.player.spirit) + '\n' +
                                                          '知识: ' + str(self.player.knowledge),
                                        justify=tk.LEFT, padx=0, pady=0)
        self.playerInfoLabel.place(x=int(parser.playerInfoLocation[0] * parser.windowSize[0]),
                                   y=int(parser.playerInfoLocation[1] * parser.windowSize[1]))

        self.throwDiceButton = tk.Button(self.window, text='掷色子', command=lambda: App.main(self))
        self.throwDiceButton.place(x=int(parser.throwDiceLocation[0] * parser.windowSize[0]),
                                   y=int(parser.throwDiceLocation[1] * parser.windowSize[1]))

        self.infoLabel = tk.Label(self.window, text='欢迎来到大复翁!', justify=tk.LEFT,
                                  width=int(parser.infoSize[0] * parser.windowSize[0]),
                                  height=int(parser.infoSize[1] * parser.windowSize[1]))
        self.infoLabel.place(x=int(parser.infoLocation[0] * parser.windowSize[0]),
                             y=int(parser.infoLocation[1] * parser.windowSize[1]))

        self.playerSmallImage = self.playerImage.resize((int(parser.playerIconSize[0] * parser.windowSize[0]),
                                                         int(parser.playerIconSize[1] * parser.windowSize[1])),
                                                        Image.ANTIALIAS)
        self.playerSmallIcon = ImageTk.PhotoImage(self.playerSmallImage)
        self.playerSmallLabel = tk.Label(self.window, image=self.playerSmallIcon)
        self.playerSmallLabel.place(x=int(self.gameMapLabel['width'] * self.locations[self.player.location][0]) +
                                      self.gameMapLabel.place_info()['x'],
                                    y=int(self.gameMapLabel['height'] * self.locations[self.player.location][1]) +
                                      self.gameMapLabel.place_info()['y'])

        self.latticeLabels = []
        self.latticeImages = []
        self.latticeIcons = []
        for k in range(len(self.lattices)):
            lattice = self.lattices[k]
            self.latticeImages.extend(Image.open(parser.materialsPath + lattice.icon))
            self.latticeImages[-1] = self.latticeImages[-1].resize((int(self.gameMapLabel['width'] * self.sizes[k][0]),
                                                                    int(self.gameMapLabel['height'] * self.sizes[k][1]),
                                                                    Image.ANTIALIAS))
            self.latticeIcons.extend(tk.PhotoImage(self.latticeImages[-1]))
            self.latticeLabels.extend(tk.Label(self.window, image=self.latticeIcons[-1]))
            self.latticeLabels[-1].bind('<Enter>', lambda event: self.showLatticeInfo(self.latticeLabels[-1]))
            self.latticeLabels[-1].place(x=int(self.gameMapLabel['width'] * self.locations[k][0]) +
                                           self.gameMapLabel.place_info()['x'],
                                         y=int(self.gameMapLabel['height'] * self.locations[k][1]) +
                                           self.gameMapLabel.place_info()['y'])

    def main(self):
        dice = self.throwDice()

        if self.player.location + dice > len(self.locations):
            self.lap = self.lap + 1

        if self.lap in [0, 1]:
            newLocation = self.player.location + dice % len(self.locations)
            self.movePlayer(newLocation)
            self.player.location = newLocation
        elif self.lap == 2:
            newLocation = self.player.location + dice % len(self.locations)
            self.movePlayer(newLocation)
            self.player.location = newLocation
            self.showFinalExam()
        elif self.lap == 3:
            self.enterNextGrade()
            newLocation = self.parser.initialLocation
            self.movePlayer(newLocation)
            self.player.location = newLocation

        lattice = self.lattices[self.player.location]
        if isinstance(lattice, Chance):
            self.drawCard()
        elif isinstance(lattice, Site):
            self.interactWithSite(lattice)

    def movePlayer(self, newLocation):
        nSteps = self.parser.nSteps
        pauseTime = self.parser.pauseTime
        oldLocation = self.player.location
        if newLocation < oldLocation:
            locationIndices = list(range(oldLocation, len(self.locations)))
            locationIndices.extend(range(newLocation + 1))
        else:
            locationIndices = list(range(oldLocation, newLocation + 1))

        for k in range(len(locationIndices) - 1):
            xFrom = int(self.gameMapLabel['width'] * self.locations[locationIndices[k]][0]) + \
                    self.gameMapLabel.place_info()['x']
            yFrom = int(self.gameMapLabel['height'] * self.locations[locationIndices[k]][0]) + \
                    self.gameMapLabel.place_info()['y']
            xTo = int(self.gameMapLabel['width'] * self.locations[locationIndices[k + 1]][0]) + \
                  self.gameMapLabel.place_info()['x']
            yTo = int(self.gameMapLabel['height'] * self.locations[locationIndices[k + 1]][0]) + \
                  self.gameMapLabel.place_info()['y']
            intervalX = round((xTo - xFrom) / nSteps)
            intervalY = round((yTo - yFrom) / nSteps)
            xs = list(range(xFrom, xTo + intervalX, intervalX))
            ys = list(range(yFrom, yTo + intervalY, intervalY))
            xs[-1] = xTo
            ys[-1] = yTo
            for x, y in zip(xs, ys):
                self.playerSmallLabel.place(x=x, y=y)
                time.sleep(pauseTime)

        self.playerSmallLabel.place(x=int(self.locations[self.player.location][0] *
                                          self.gameMapLabel['width']) + self.gameMapLabel.place_info()['x'],
                                    y=int(self.locations[self.player.location][1] *
                                          self.gameMapLabel['height']) + self.gameMapLabel.place_info()['y'])
        self.infoLabel['text'] = self.truncateText(self.infoLabel['text'] + '\n你从"' +
                                                   self.lattices[oldLocation].name + "来到了" +
                                                   self.lattices[newLocation].name + "!")

    def showFinalExam(self):
        self.lattices = self.parser.latticesWithFinalExam
        self.locations = self.parser.locationsWithFinalExam
        self.sizes = self.parser.sizesWithFinalExam
        self.updateMap()
        self.infoLabel['text'] = self.truncateText(self.infoLabel['text'] + '\n期末考试到来了!')

    def enterNextGrade(self):
        index = self.parser.grades.index(self.player.grade)
        if index == len(self.parser.grades) - 1:
            self.endOfGame()
        else:
            self.lap = 0
            self.player.grade = self.parser.grades[index + 1]
            self.lattices = self.parser.initialLattices
            self.locations = self.parser.initialLocations
            self.sizes = self.parser.initialSizes
            self.updatePlayerInfo()
            self.updateMap()
            self.infoLabel['text'] = self.truncateText(self.infoLabel['text'] + '\n你进入了下一年级!')

    def drawCard(self):
        if len(self.parser.remainedCards) is 0:
            self.parser.remainedCards = self.parser.chances

        card = random.sample(self.parser.remainedCards, 1)
        self.player.record.extend(card)
        self.parser.remainedChances.remove(card)
        self.infoLabel['text'] = self.truncateText(self.infoLabel['text'] + '\n你抽到的卡牌是:\n' + card['name'] +
                                                   ',效果是:\n金钱: ' + ("+" + str(card['effect'][0]) if
                                                                    card['effect'][0] > 0 else str(card['effect'][0])) +
                                                   "\n时间: " + ("+" + str(card['effect'][1]) if
                                                               card['effect'][1] > 0 else str(card['effect'][1])) +
                                                   "\n体力: " + ("+" + str(card['effect'][2]) if
                                                               card['effect'][2] > 0 else str(card['effect'][2])) +
                                                   "\n知识: " + ("+" + str(card['effect'][3]) if
                                                               card['effect'][3] > 0 else str(card['effect'][3])))
        time.sleep(0.5)
        if card['isCompulsory']:
            self.infoLabel['text'] = self.truncateText(self.infoLabel['text'] + '\n卡牌是强制的,你使用了卡牌')
            self.useCard(card)
        else:
            self.infoLabel['text'] = self.truncateText(self.infoLabel['text'] + '\n卡牌不是强制的,你需要决定\n是否使用卡牌')
            time.sleep(0.5)
            newWindow = tk.Tk()
            newWindow.geometry('300x500')
            confirmButton = tk.Button(newWindow, text="使用这张卡牌", commamd=lambda: self.useCard(card))
            discardButton = tk.Button(newWindow, text="不使用这张卡牌", commamd=newWindow.destroy())
            confirmButton.pack(side=tk.TOP, fill=tk.Y, expand=tk.YES)
            discardButton.pack(side=tk.BOTTOM, fill=tk.Y, expand=tk.YES)
            newWindow.mainloop()

    def interactWithSite(self, site):
        if not site.name == '期末考试':
            self.infoLabel['text'] = self.truncateText(self.infoLabel['text'] + '\n' + site.name + '的效果是' +
                                                       '\n金钱: ' + ("+" + str(site.effect[0]) if
                                                                   site.effect[0] > 0 else str(site.effect[0])) +
                                                       "\n时间: " + ("+" + str(site.effect[1]) if
                                                                   site.effect[1] > 0 else str(site.effect[1])) +
                                                       "\n体力: " + ("+" + str(site.effect[2]) if
                                                                   site.effect[2] > 0 else str(site.effect[2])) +
                                                       "\n知识: " + ("+" + str(site.effect[3]) if
                                                                   site.effect[3] > 0 else str(site.effect[3])))
            time.sleep(0.5)
            if site.isCompulsory:
                self.infoLabel['text'] = self.truncateText(self.infoLabel['text'] + '\n在' + site.name + '你进行了' +
                                                           site.action + '\n' + site.text)
            else:
                self.infoLabel['text'] = self.truncateText(self.infoLabel['text'] + '\n在' + site.name + '你可以选择是否' +
                                                           site.action)
                time.sleep(0.5)
                newWindow = tk.Tk()
                newWindow.geometry('300x500')
                confirmButton = tk.Button(newWindow, text="在" + site.name + site.action,
                                          commamd=lambda: self.makeAction(site))
                refuseButton = tk.Button(newWindow, text="不在" + site.name + site.action, commamd=newWindow.destroy())
                confirmButton.pack(side=tk.TOP, fill=tk.Y, expand=tk.YES)
                refuseButton.pack(side=tk.BOTTOM, fill=tk.Y, expand=tk.YES)
                newWindow.mainloop()
        else:
            self.infoLabel['text'] = self.truncateText(self.infoLabel['text'] + '\n你遇上了期末考试')
            self.enterNextGrade()

    def updateMap(self):
        for k in range(len(self.lattices)):
            self.latticeImages[k] = Image.open(self.parser.materialsPath + self.lattices[k].icon)
            self.latticeImages[k] = self.latticeImages[k].resize((int(self.gameMapLabel['width'] * self.sizes[k][0]),
                                                                  int(self.gameMapLabel['height'] * self.sizes[k][1]),
                                                                  Image.ANTIALIAS))
            self.latticeIcons[k] = tk.PhotoImage(self.latticeImages[k])
            self.latticeLabels[k]['image'] = self.latticeIcons[-1]
            self.latticeLabels[k].place(x=int(self.gameMapLabel['width'] * self.locations[k][0]) +
                                          self.gameMapLabel.place_info()['x'],
                                        y=int(self.gameMapLabel['height'] * self.locations[k][1]) +
                                          self.gameMapLabel.place_info()['y'])
        self.infoLabel['text'] = self.truncateText(self.infoLabel['text'] + '\n游戏地图更新了!')

    def updatePlayerInfo(self):
        self.playerInfoLabel['text'] = '姓名: ' + str(self.player.name) + '\n' + \
                                       '年级: ' + str(self.player.grade) + '\n' + \
                                       '金钱: ' + str(self.player.money) + '\n' + \
                                       '时间: ' + str(self.player.time) + '\n' + \
                                       '体力: ' + str(self.player.time) + '\n' + \
                                       '知识: ' + str(self.player.knowledge)
        self.infoLabel['text'] = self.truncateText(self.infoLabel['text'] + '\n你的属性更新了!')

    def throwDice(self):
        dice = random.randint(1, 6)
        self.infoLabel['text'] = self.truncateText(self.infoLabel['text'] + '\n掷色子结果是: ' + str(dice) + "!")
        return dice

    def useCard(self, card):
        self.player.money = self.player.money + card['effect'][0]
        self.player.time = self.player.time + card['effect'][1]
        self.player.spirit = self.player.spirit + card['effect'][2]
        self.player.knowledge = self.player.knowledge + card['effect'][3]
        self.updatePlayerInfo()

    def makeAction(self, site):
        self.player.money = self.player.money + site.effect[0]
        self.player.time = self.player.time + site.effect[1]
        self.player.spirit = self.player.spirit + site.effect[2]
        self.player.knowledge = self.player.knowledge + site.effect[3]
        self.updatePlayerInfo()

    def showLatticeInfo(self, lattice):
        if isinstance(lattice, Site):
            self.infoLabel['text'] = self.truncateText(self.infoLabel['text'] + '\n' +
                                                       lattice.name + ": " + lattice.action)
        elif isinstance(lattice, Chance):
            if lattice.name == "Chance":
                self.infoLabel['text'] = self.truncateText(self.infoLabel['text'] + '\n机会: 可抽取一张\n机会牌')
            elif lattice.name == "Fate":
                self.infoLabel['text'] = self.truncateText(self.infoLabel['text'] + '\n命运: 可抽取一张\n命运牌')
        elif isinstance(lattice, BlankLattice):
            self.infoLabel['text'] = self.truncateText(self.infoLabel['text'] + '\n这是一个空格子')

    def truncateText(self, text):
        n = text.count('\n') + 1
        if n <= self.parser.maxLines:
            return text
        else:
            index = 0
            for i in range(n - self.parser.maxLines):
                index = index + text[index + 1:].index('\n')
            return text[index + 1:]

    def endOfGame(self):
        endWindow = tk.Tk()
        endWindow.geometry('200x300')
        print(self)

    def showPlayerInfo(self):
        newWindow = tk.Tk()
        newWindow.geometry('300x300')

        playerImage = Image.open(self.parser.materialsPath + self.parser.playerIcon)
        playerImage = playerImage.resize((200, 200), Image.ANTIALIAS)
        playerIcon = ImageTk.PhotoImage(playerImage)
        playerLabel = tk.Label(newWindow, image=playerIcon)
        playerLabel.pack(side=tk.TOP)

        playerName = tk.Entry(newWindow)
        playerName.insert("end", self.player.name)
        playerName.pack(side=tk.TOP)

        renameButton = tk.Button(newWindow, text="修改昵称",
                                 command=lambda: exec('self.renamePlayer(playerName.get(), newWindow); '
                                                      'newWindow.destroy()'))
        renameButton.place(x=50, y=250)
        modifyIconButton = tk.Button(newWindow, text="修改头像",
                                     command=lambda: exec('self.modifyPlayerIcon(newWindow)); newWindow.destroy()'))
        modifyIconButton.pack(x=200, y=250)

        newWindow.mainloop()

    def modifyPlayerIcon(self):
        newWindow = tk.Tk()
        newWindow.withdraw()

        defaultDirectory = os.getcwd()
        iconPath = filedialog.askopenfilename(title="选择头像", initialdir=defaultDirectory)
        self.player.icon = iconPath
        self.playerImage = Image.open(iconPath)
        self.playerImage = self.playerImage.resize((int(self.parser.playerIconSize[0] * self.parser.windowSize[0]),
                                                    int(self.parser.playerIconSize[1] * self.parser.windowSize[1])),
                                                   Image.ANTIALIAS)
        self.playerIcon = ImageTk.PhotoImage(self.playerImage)
        self.playerButton['image'] = self.playerIcon

    def renamePlayer(self, newName):
        self.player.name = newName
        playerConfig = pickle.load(open(self.parser.playerConfigPath, 'rb'))
        playerConfig['playerName'] = newName
        pickle.dump(playerConfig, open(self.parser.playerConfigPath, 'wb'))
        self.updatePlayerInfo()
