from PIL import ImageTk, Image
import time

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
                                      command=lambda: self.player(self.parser))
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

        self.playerInfoLabel = tk.Label(self.window, text='Name: ' + str(self.player.name) + '\n' +
                                                          'Grade: ' + str(self.player.grade) + '\n' +
                                                          'Money: ' + str(self.player.money) + '\n' +
                                                          'Time: ' + str(self.player.time) + '\n' +
                                                          'Spirit: ' + str(self.player.spirit),
                                        justify=tk.LEFT, padx=0, pady=0)
        self.playerInfoLabel.place(x=int(parser.playerInfoLocation[0] * parser.windowSize[0]),
                                   y=int(parser.playerInfoLocation[1] * parser.windowSize[1]))

        self.throwDiceButton = tk.Button(self.window, text='Throw dice', command=lambda: App.main(self))
        self.throwDiceButton.place(x=int(parser.throwDiceLocation[0] * parser.windowSize[0]),
                                   y=int(parser.throwDiceLocation[1] * parser.windowSize[1]))

        self.infoLabel = tk.Label(self.window, text='Welcome to\nFudan Monopoly!', justify=tk.LEFT,
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
            pass
        elif not isinstance(lattice, BlankLattice):
            raise RuntimeError('Invalid Lattice!')

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
            xFrom = int(self.gameMapLabel['width'] * self.locations[locationIndices[k]][0]) +\
                    self.gameMapLabel.place_info()['x']
            yFrom = int(self.gameMapLabel['height'] * self.locations[locationIndices[k]][0]) +\
                    self.gameMapLabel.place_info()['y']
            xTo = int(self.gameMapLabel['width'] * self.locations[locationIndices[k + 1]][0]) +\
                  self.gameMapLabel.place_info()['x']
            yTo = int(self.gameMapLabel['height'] * self.locations[locationIndices[k + 1]][0]) +\
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

    def updatePlayerInfo(self):
        self.playerInfoLabel['text'] = 'Name: ' + str(self.player.name) + '\n' + \
                                       'Grade: ' + str(self.player.grade) + '\n' + \
                                       'Money: ' + str(self.player.money) + '\n' + \
                                       'Time: ' + str(self.player.time) + '\n' + \
                                       'Spirit: ' + str(self.player.time)

    def showFinalExam(self):
        self.lattices = self.parser.latticesWithFinalExam
        self.locations = self.parser.locationsWithFinalExam
        self.sizes = self.parser.sizesWithFinalExam
        self.updateMap()

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

    def endOfGame(self):
        endWindow = tk.Tk()
        endWindow.geometry('200x300')
        print(self)

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
            remainedCards = self.parser.remainedChances
        if len(remainedCards) is 0:
            remainedCards = self.parser.chances

        card = random.sample(remainedCards, 1)
        self.player.record.append(card)
        self.parser.remainedChances.remove(card)
        return card

class NewPlayer():
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name


    #设置窗口
    def set_init_window(self):
        self.init_window_name.title("新游戏")           #窗口名
        self.init_window_name.geometry('200x200+10+10')
        self.init_window_name["bg"] = "grey"
        #self.init_window_name.attributes("-alpha",0.9)                          #虚化，值越小虚化程度越高
        
        #标签
        self.init_PlayerName_label = Label(self.init_window_name, text="姓名")
        self.init_PlayerName_label.place(x=0, y=100)
        self.init_PlayerIcon_label = Label(self.init_window_name, text="头像")
        self.init_PlayerIcon_label.place(x=0, y=0)
        
        #文本框
        self.init_PlayerName_Text = Text(self.init_window_name, width=10, height=2)  #原始数据录入框
        self.init_PlayerName_Text.place(x=40,y=100)
        #按钮
        self.GameStart = Button(self.init_window_name, text="Start Game", bg="lightblue", width=10,command=self.StartGame()) 
        self.GameStart.place(x=50,y=150)


    #功能函数
    def StartGame(self):
        #这里把相应信息储存在records 待完成
        self.init_window_name.quit()
        print('new game starts')



def SetANewPlayer():
    #建立新玩家的界面
    init_window = Tk()
    top = NewPlayer(init_window)
    top.set_init_window()

    init_window.mainloop()   
