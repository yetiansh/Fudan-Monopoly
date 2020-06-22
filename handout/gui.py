import os
import pickle
import time
from tkinter import filedialog

from PIL import ImageTk, Image

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
                                      command=self.showPlayerInfo)
        self.playerButton.place(x=int(parser.playerIconLocation[0] * parser.windowSize[0]),
                                y=int(parser.playerIconLocation[1] * parser.windowSize[1]))

        self.gameMapImage = Image.open(parser.materialsPath + parser.gameMap)
        self.gameMapImage = self.gameMapImage.resize((int(parser.gameMapSize[0] * parser.windowSize[0]),
                                                      int(parser.gameMapSize[1] * parser.windowSize[1])),
                                                     Image.ANTIALIAS)
        self.gameMapIcon = ImageTk.PhotoImage(self.gameMapImage)
        self.gameMapLabel = tk.Label(self.window, image=self.gameMapIcon,
                                     width=int(parser.gameMapSize[0] * parser.windowSize[0]),
                                     height=int(parser.gameMapSize[1] * parser.windowSize[1]))
        self.gameMapLabel.place(x=int(parser.gameMapLocation[0] * parser.windowSize[0]),
                                y=int(parser.gameMapLocation[1] * parser.windowSize[1]))

        self.playerInfoLabel = tk.Label(self.window, text='姓名: ' + str(self.player.name) + '\n' +
                                                          '年级: ' + str(self.player.grade) + '\n' +
                                                          '金钱: ' + str(self.player.money) + '\n' +
                                                          '时间: ' + str(self.player.time) + '\n' +
                                                          '体力: ' + str(self.player.spirit) + '\n' +
                                                          '知识: ' + str(self.player.knowledge),
                                        justify=tk.LEFT)
        self.playerInfoLabel.place(x=int(parser.playerInfoLocation[0] * parser.windowSize[0]),
                                   y=int(parser.playerInfoLocation[1] * parser.windowSize[1]))

        self.throwDiceButton = tk.Button(self.window, text='掷色子', command=self.main)
        self.throwDiceButton.place(x=int(parser.throwDiceLocation[0] * parser.windowSize[0]),
                                   y=int(parser.throwDiceLocation[1] * parser.windowSize[1]))

        self.infoLabel = tk.Label(self.window, text='欢迎来到大复翁\n', justify=tk.LEFT, wraplength=120,
                                  width=int(parser.infoSize[0] * parser.windowSize[0]),
                                  height=int(parser.infoSize[1] * parser.windowSize[1]))
        self.infoLabel.place(x=int(parser.infoLocation[0] * parser.windowSize[0]),
                             y=int(parser.infoLocation[1] * parser.windowSize[1]))

        self.latticeLabels = []
        self.latticeImages = []
        self.latticeIcons = []
        for k in range(len(self.lattices)):
            lattice = self.lattices[k]
            self.latticeImages = self.latticeImages + [Image.open(parser.materialsPath + lattice.icon)]
            self.latticeImages[-1] = self.latticeImages[-1].resize((int(self.gameMapLabel['width'] * self.sizes[k][0]),
                                                                    int(self.gameMapLabel['height'] * self.sizes[k][1])),
                                                                    Image.ANTIALIAS)
            self.latticeIcons = self.latticeIcons + [ImageTk.PhotoImage(self.latticeImages[-1])]
            self.latticeLabels = self.latticeLabels + [tk.Label(self.window, image=self.latticeIcons[-1])]
            self.latticeLabels[-1].bind('<Button-1>', lambda event: self.showLatticeInfo(self.latticeLabels[-1]))
            self.latticeLabels[-1].place(x=int(self.gameMapLabel['width'] * self.locations[k][0]) +
                                           int(self.gameMapLabel.place_info()['x']),
                                         y=int(self.gameMapLabel['height'] * self.locations[k][1]) +
                                           int(self.gameMapLabel.place_info()['y']))

        self.playerSmallImage = self.playerImage.resize((int(parser.playerSmallIconSize[0] * parser.windowSize[0]),
                                                         int(parser.playerSmallIconSize[1] * parser.windowSize[1])),
                                                        Image.ANTIALIAS)
        self.playerSmallIcon = ImageTk.PhotoImage(self.playerSmallImage)
        self.playerSmallLabel = tk.Label(self.window, image=self.playerSmallIcon)
        self.playerSmallLabel.place(x=int(self.gameMapLabel['width'] * self.locations[self.player.location][0]) +
                                      int(self.gameMapLabel.place_info()['x']),
                                    y=int(self.gameMapLabel['height'] * self.locations[self.player.location][1]) +
                                      int(self.gameMapLabel.place_info()['y']))

    def main(self):
        dice = self.throwDice()

        if self.player.location + dice > len(self.locations):
            self.lap = self.lap + 1

        if self.lap in [0, 1]:
            newLocation = (self.player.location + dice) % len(self.locations)
            self.movePlayer(newLocation)
            self.player.location = newLocation
        elif self.lap == 2:
            newLocation = (self.player.location + dice) % len(self.locations)
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
            if not lattice.name == '起点':
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
                    int(self.gameMapLabel.place_info()['x'])
            yFrom = int(self.gameMapLabel['height'] * self.locations[locationIndices[k]][0]) + \
                    int(self.gameMapLabel.place_info()['y'])
            xTo = int(self.gameMapLabel['width'] * self.locations[locationIndices[k + 1]][0]) + \
                  int(self.gameMapLabel.place_info()['x'])
            yTo = int(self.gameMapLabel['height'] * self.locations[locationIndices[k + 1]][0]) + \
                  int(self.gameMapLabel.place_info()['y'])
            intervalX = round((xTo - xFrom) / nSteps)
            intervalY = round((yTo - yFrom) / nSteps)
            if intervalX is not 0:
                xs = list(range(xFrom, xTo + intervalX, intervalX))
            else:
                xs = [xTo] * nSteps

            if intervalY is not 0:
                ys = list(range(yFrom, yTo + intervalY, intervalY))
            else:
                ys = [yTo] * nSteps

            xs[-1] = xTo
            ys[-1] = yTo
            for x, y in zip(xs, ys):
                self.playerSmallLabel.place(x=x, y=y)
                # time.sleep(pauseTime)

        self.playerSmallLabel.place(x=int(self.locations[self.player.location][0] *
                                          self.gameMapLabel['width']) + int(self.gameMapLabel.place_info()['x']),
                                    y=int(self.locations[self.player.location][1] *
                                          self.gameMapLabel['height']) + int(self.gameMapLabel.place_info()['y']))
        self.infoLabel['text'] = self.truncateText(self.infoLabel['text'] + '\n你从' +
                                                   self.lattices[oldLocation].name + "来到了" +
                                                   self.lattices[newLocation].name)

    def showFinalExam(self):
        self.lattices = self.parser.latticesWithFinalExam
        self.locations = self.parser.locationsWithFinalExam
        self.sizes = self.parser.sizesWithFinalExam
        # self.updateMap()
        # self.infoLabel['text'] = self.truncateText(self.infoLabel['text'] + '\n期末考试出现了')

    def enterNextGrade(self):
        index = self.parser.grades.index(self.player.grade)
        if index == len(self.parser.grades) - 1:
            self.endOfGame()
        else:
            self.player.attributes.append(
                [self.player.money, self.player.time, self.player.spirit, self.player.knowledge])

            self.lap = 0
            self.player.grade = self.parser.grades[index + 1]
            self.lattices = self.parser.initialLattices
            self.locations = self.parser.initialLocations
            self.sizes = self.parser.initialSizes

            self.player.money = self.parser.initialMoney
            self.player.time = self.parser.initialTime
            self.player.spirit = self.parser.initialSpirit
            self.player.knowledge = self.parser.initialKnowledge

            time.sleep(self.parser.pauseTime)
            self.updatePlayerInfo()
            # self.updateMap()
            self.infoLabel['text'] = self.truncateText(self.infoLabel['text'] + '\n你在期末考试后进入了下一年级')

    def drawCard(self):
        [card] = random.sample(self.parser.remainedChances, 1)
        self.infoLabel['text'] = self.truncateText(self.infoLabel['text'] + '\n你抽到的卡牌是:\n' + card['name'] +
                                                   '\n效果是:\n金钱: ' + ("+" + str(card['effect'][0]) if
                                                                    card['effect'][0] > 0 else str(card['effect'][0])) +
                                                   "\n时间: " + ("+" + str(card['effect'][1]) if
                                                               card['effect'][1] > 0 else str(card['effect'][1])) +
                                                   "\n体力: " + ("+" + str(card['effect'][2]) if
                                                               card['effect'][2] > 0 else str(card['effect'][2])) +
                                                   "\n知识: " + ("+" + str(card['effect'][3]) if
                                                               card['effect'][3] > 0 else str(card['effect'][3])))
        time.sleep(self.parser.pauseTime)
        if card['isCompulsory']:
            self.infoLabel['text'] = self.truncateText(self.infoLabel['text'] + '\n卡牌是强制的,你使用了卡牌')
            self.useCard(card)
        else:
            self.infoLabel['text'] = self.truncateText(self.infoLabel['text'] + '\n卡牌不是强制的,你需要决定\n是否使用卡牌')
            time.sleep(self.parser.pauseTime)
            newWindow = tk.Tk()
            newWindow.geometry('300x500')
            confirmButton = tk.Button(newWindow, text="使用这张卡牌", command=lambda: self.useCard(card))
            discardButton = tk.Button(newWindow, text="不使用这张卡牌", command=newWindow.destroy)
            confirmButton.pack(side=tk.TOP, fill=tk.Y, expand=tk.YES)
            discardButton.pack(side=tk.BOTTOM, fill=tk.Y, expand=tk.YES)
            newWindow.mainloop()

    def interactWithSite(self, site):
        def act():
            self.makeAction(site)
            newWindow.destroy()

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
            time.sleep(self.parser.pauseTime)
            if site.isCompulsory:
                self.makeAction(site)
            else:
                self.infoLabel['text'] = self.truncateText(self.infoLabel['text'] + '\n在' + site.name + '你可以选择是否' +
                                                           site.action)
                time.sleep(self.parser.pauseTime)
                newWindow = tk.Tk()
                newWindow.geometry('300x50')
                newWindow.title('选择动作')
                confirmButton = tk.Button(newWindow, text="在" + site.name + site.action, relief=tk.FLAT,
                                          command=act)
                refuseButton = tk.Button(newWindow, text="不在" + site.name + site.action, relief=tk.FLAT,
                                         command=newWindow.destroy)
                confirmButton.pack(side=tk.LEFT, fill=tk.Y, expand=tk.YES)
                refuseButton.pack(side=tk.RIGHT, fill=tk.Y, expand=tk.YES)
                newWindow.mainloop()
        else:
            self.infoLabel['text'] = self.truncateText(self.infoLabel['text'] + '\n你遇上了期末考试')
            self.enterNextGrade()

    def updateMap(self):
        for k in range(len(self.lattices)):
            self.latticeImages[k] = Image.open(self.parser.materialsPath + self.lattices[k].icon)
            self.latticeImages[k] = self.latticeImages[k].resize((int(self.gameMapLabel['width'] * self.sizes[k][0]),
                                                                  int(self.gameMapLabel['height'] * self.sizes[k][1])),
                                                                  Image.ANTIALIAS)
            self.latticeIcons[k] = tk.PhotoImage(self.latticeImages[k])
            self.latticeLabels[k].image = self.latticeIcons[k]
            self.latticeLabels[k].place(x=int(self.gameMapLabel['width'] * self.locations[k][0]) +
                                          int(self.gameMapLabel.place_info()['x']),
                                        y=int(self.gameMapLabel['height'] * self.locations[k][1]) +
                                          int(self.gameMapLabel.place_info()['y']))
        self.infoLabel['text'] = self.truncateText(self.infoLabel['text'] + '\n游戏地图更新了')

    def updatePlayerInfo(self):
        self.playerInfoLabel['text'] = '姓名: ' + str(self.player.name) + '\n' + \
                                       '年级: ' + str(self.player.grade) + '\n' + \
                                       '金钱: ' + str(self.player.money) + '\n' + \
                                       '时间: ' + str(self.player.time) + '\n' + \
                                       '体力: ' + str(self.player.spirit) + '\n' + \
                                       '知识: ' + str(self.player.knowledge)
        self.infoLabel['text'] = self.truncateText(self.infoLabel['text'] + '\n你的属性更新了')

    def throwDice(self):
        dice = random.randint(1, 6)
        self.infoLabel['text'] = self.truncateText(self.infoLabel['text'] + '\n掷色子结果是: ' + str(dice) + "")
        return dice

    def useCard(self, card):
        if not card['name'] in self.player.records.keys():
            self.player.records[card['name']] = 1
        else:
            self.player.records[card['name']] = self.player.records[card['name']] + 1

        self.player.money = self.player.money + card['effect'][0]
        self.player.time = self.player.time + card['effect'][1]
        self.player.spirit = self.player.spirit + card['effect'][2]
        self.player.knowledge = self.player.knowledge + card['effect'][3]
        self.updatePlayerInfo()

    def makeAction(self, site):
        if not "在" + site.name + site.action in self.player.records.keys():
            self.player.records["在" + site.name + site.action] = 1
        else:
            self.player.records["在" + site.name + site.action] = \
                self.player.records["在" + site.name + site.action] + 1

        self.infoLabel['text'] = self.truncateText(self.infoLabel['text'] + '\n在' + site.name + '你进行了' +
                                                   site.action + '\n' + site.text)
        self.player.money = self.player.money + site.effect[0]
        self.player.time = self.player.time + site.effect[1]
        self.player.spirit = self.player.spirit + site.effect[2]
        self.player.knowledge = self.player.knowledge + site.effect[3]
        self.updatePlayerInfo()

    def showLatticeInfo(self, lattice):
        if isinstance(lattice, Site):
            self.infoLabel['text'] = self.truncateText(self.infoLabel['text'] + '\n' +
                                                       lattice.name + ": " + lattice.text)
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
                index = index + text[index + 1:].index('\n') + 1
            return text[index + 1:]

    def endOfGame(self):
        def showLines():
            for line in lines:
                message['text'] = message['text'] + line + '\n'
                time.sleep(self.parser.pauseTime)

        with open('handout/materials/gameRecord-' + self.player.name + time.strftime('%Y-%m-%d %H-%M-%S.dat'),
                  'wb') as file:
            pickle.dump(self.player.attributes, file)
            pickle.dump(self.player.records, file)

        records = sorted(self.player.records.items(), key=lambda k: k[1])
        knowledge = sum([result[3] for result in self.player.attributes])
        spirit = sum([result[2] for result in self.player.attributes])

        if knowledge < 15:
            knowledgeLine = '学习对你来说似乎相当挣扎, 补考是你每个学期开始前一定经历的事情, 你不懂身边的人是怎么搞清楚淑芬大雾的, 对你来说真的太难了, 最后, 一张均绩2.0的成绩单, 让你低空飘过\n'
        elif 15 <= knowledge < 25:
            knowledgeLine = '大学的学习节奏有点让你不太适应, 各种各样的pj和pre似乎总是堆在一起来到ddl, 很难处理过来, 这种压力将你的绩点定格在了2.7\n'
        elif 25 <= knowledge < 35:
            knowledgeLine = '从高中升上大学, 虽然开始有些不太适应, 但通过你起早贪黑地学习, 教学楼成了你的第二宿舍, 绩点也在稳步提高, 每个在教室度过的夜晚都成为你3.3均绩的基石\n'
        else:
            knowledgeLine = '对你来说, 学习就是小菜一碟, 不管是专业课、模块课, 还是英语课、体育课, 全部都不在话下, 教学楼就是你的第二宿舍, 均绩4.0, 你就是学习的神\n'

        if spirit < 15:
            spiritLine = '体育活动就是你的天敌, 每个学期的早锻、必锻就期待着一些能提供刷卡但不需要动的活动来完成, 各种体育比赛更是和你无缘, 最终久坐不动压垮了你的身体, 让你常常感觉到身体不舒服\n'
        elif 15 <= spirit < 25:
            spiritLine = '体育活动对你来说有些勉强, 出于身体健康的考虑, 你仍然会去参加一些校内体育比赛, 每个学期的 锻炼总是堪堪刷完, 直到工作以后, 你才发现养成一些良好锻炼习惯的重要性\n'
        elif 25 <= spirit < 35:
            spiritLine = '体育活动作为你的兴趣, 从来不会对你产生负担, 开始刷锻第三周你就能刷完, 院系杯、信院杯、校运动会总有你的身影, 名次也相当不错。身体是革命的本钱, ' \
                         '一副健康的体魄为你以后长久的工作打下了基础\n '
        else:
            spiritLine = '体育比赛是你本科生活的重要一环, 制霸了校内的所有杯赛。同时作为复旦校队队长, 你率队参加大学生业余组比赛, 拿下两届冠军, 刷锻？免了三学期的锻, 并不需要刷\n'

        lines = "四年的时光一晃而过, 转眼间, 已经来到了毕业的日子\n6月, 初夏, 天气还不是那么炎热, 你回忆起了过去四年的经历……\n" + \
                "四年里，你一共" + records[0][0] + str(records[0][1]) + "次, " + \
                records[1][0] + str(records[1][1]) + "次, " + \
                records[2][0] + str(records[2][1]) + "次\n" + knowledgeLine + '\n' + spiritLine

        if knowledge + spirit > 80:
            lines = lines + "德智体美劳全面发展的你在毕业典礼上荣获毕业生之星称号\n"
        if '期中退课' in self.player.records.keys():
            if self.player.records['期中退课'] > 3:
                lines = lines + "退课是你复旦生活中过不去的一道坎, 每个学期都退课让你成为了一个传说\n"

        plays = 0
        if '旦苑小卖部' in self.player.records.keys():
            plays = plays + self.player.records['旦苑小卖部']
        if '靠一点点续命' in self.player.records.keys():
            plays = plays + self.player.records['靠一点点续命']
        if '阿康的诱惑' in self.player.records.keys():
            plays = plays + self.player.records['阿康的诱惑']
        if '五角场' in self.player.records.keys():
            plays = plays + self.player.records['五角场']

        if plays > 8:
            lines = lines + "甜食和烧烤的快乐是你无法拒绝的, 当然这也导致了四年间你疯狂增长的体重\n"

        lines = lines + "总而言之, 恭喜你顺利毕业, 祝贺你跻身百年复旦的星空, 日月光华中有你闪亮的眼睛, 你计划的秋天已褪去童话的色彩, 一个真实的现在可以开垦一万个美丽的未来"
        lines = lines.split('\n')

        newWindow = tk.Toplevel()
        newWindow.geometry('400x550')
        newWindow.title('毕业报告')
        message = tk.Message(newWindow, width=200)
        message.pack(side=tk.TOP)
        button = tk.Button(newWindow, text="展示你的毕业报告", command=showLines)
        button.pack(side=tk.BOTTOM)
        newWindow.mainloop()

    def showPlayerInfo(self):
        def rename():
            self.renamePlayer(playerName.get())
            newWindow.destroy()

        def modify():
            self.modifyPlayerIcon()
            newWindow.destroy()

        newWindow = tk.Toplevel()
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
                                 command=rename)
        renameButton.place(x=50, y=250)
        modifyIconButton = tk.Button(newWindow, text="修改头像",
                                     command=modify)
        modifyIconButton.place(x=200, y=250)

        newWindow.mainloop()

    def modifyPlayerIcon(self):
        newWindow = tk.Toplevel()
        newWindow.withdraw()

        defaultDirectory = os.getcwd()
        iconPath = filedialog.askopenfilename(title="选择头像", initialdir=defaultDirectory)

        playerConfig = pickle.load(open(self.parser.playerConfigPath, 'rb'))
        playerConfig['playerIcon'] = iconPath
        pickle.dump(playerConfig, open(self.parser.playerConfigPath, 'wb'))

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
