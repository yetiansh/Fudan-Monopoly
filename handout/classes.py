import random

grades = ['freshman', 'sophomore', 'junior', 'senior']
sites = []  # 设计好的地点
chances = []  # 设计好的命运牌
positions = []  # 设计好的位置
lattices = []   # 设计好的格子
remainedChances = chances


class Player:
    def __init__(self, parser):
        self.name = parser.playerName
        self.icon = parser.playerIcon
        self.location = parser.initialLocation
        self.money = parser.initialMoney
        self.spirit = parser.initialSpirit
        self.knowledge = parser.initialKnowledge
        self.grade = grades[0]

    def throwDice(self):
        results = [random.randint(1, 6), random.randint(1, 6)]
        return results

    def __call__(self):
        #   作为回调函数，调用时弹出一个界面显示玩家的属性、头像等信息，待完成
        pass


class Lattice:
    def __init__(self,
                 name=None,
                 text=None,
                 icon=None):
        self.name = name
        self.text = text
        self.icon = icon

    def __call__(self):
        #   会被子类覆盖的调用方法
        pass


class Site(Lattice):
    def __init__(self,
                 name=None,
                 text=None,
                 icon=None,
                 effect=None,
                 isCompulsory=None,
                 isLinked=False,
                 linkedMiniGame=None):
        super().__init__(name, text, icon)
        self.effect = effect
        self.isCompulsory = isCompulsory
        self.isLinked = isLinked
        self.linkedMiniGame = linkedMiniGame
        if self.isLinked and linkedMiniGame is None:
            raise RuntimeError('Linked mini game must be specified.')

    def __call__(self):
        #   作为回调函数，调用时弹出一个界面显示地点的信息，待完成
        pass


def drawCard(remainedCards=None):
    #   用于抽卡的函数，在gui中被调用
    if remainedCards is None:
        remainedCards = remainedChances
    if len(remainedCards) is 0:
        remainedCards = chances

    card = random.sample(remainedCards, 1)
    remainedChances.remove(card)
    return card


class Chance(Lattice):
    def __init__(self,
                 name=None,
                 text=None,
                 icon=None):
        super().__init__(name, text, icon)

    def __call__(self):
        #   作为回调函数，调用时弹出一个界面显示命运牌的信息，待完成
        pass


class BlankLattice(Lattice):
    def __init__(self,
                 name=None,
                 text=None,
                 icon=None):
        super().__init__(name, text, icon)

    def __call__(self):
        #   作为回调函数，调用时弹出界面显示空白格子的信息，待完成
        pass


class Board:
    def __init__(self, lattices, positions, player):
        self.lattices = lattices
        self.positions = positions
        self.player = player
