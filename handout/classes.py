import tkinter as tk
import random


class Player:
    def __init__(self, parser):
        self.name = parser.playerName
        self.icon = parser.playerIcon
        self.location = parser.initialLocation
        self.money = parser.initialMoney
        self.time = parser.initialTime
        self.spirit = parser.initialSpirit
        self.knowledge = parser.initialKnowledge
        self.grade = parser.grades[0]
        self.record = []

    def __call__(self, parser):
        #   作为回调函数，调用时弹出一个界面显示玩家的属性、头像等信息，待完成
        window = tk.Tk()
        window.mainloop()


class Lattice:
    def __init__(self,
                 name=None,
                 text=None,
                 icon=None):
        self.name = name
        self.text = text
        self.icon = icon


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


class Chance(Lattice):
    def __init__(self,
                 name=None,
                 text=None,
                 icon=None,
                 isCompulsory=None):
        super().__init__(name, text, icon)
        self.isCompulsory = isCompulsory


class BlankLattice(Lattice):
    def __init__(self,
                 name=None,
                 text=None,
                 icon=None):
        super().__init__(name, text, icon)
