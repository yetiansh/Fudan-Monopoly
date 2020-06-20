import pickle
from handout.classes import *

#   金钱、时间、体力、知识

grades = ['大一', '大二', '大三', '大四']
sites = [Site(name="第三教学楼", text="听课", effect=[0, -1, 0, 1], isCompulsory=False),
         Site(name="第二教学楼", text="听课", effect=[0, -1, 0, 1], isCompulsory=False),
         Site(name="光华楼小圆桌", text="自习", effect=[0, -1, 0, 1], isCompulsory=False),
         Site(name="第五教学楼", text="自习", effect=[0, -1, 0, 1], isCompulsory=False),
         Site(name="第六教学楼", text="自习", effect=[0, -1, 0, 1], isCompulsory=False),
         Site(name="恒隆物理楼", text="做实验。我的电压表终于接完了，到通电的回合了！测试！咦，这股焦香是……", effect=[0, -1, 0, 1], isCompulsory=False),
         Site(name="光华楼东侧会议室", text="听讲座", effect=[0, -1, 0, 1], isCompulsory=False),
         Site(name="书呆子", text="买书", effect=[-1, 0, 0, 1], isCompulsory=False),
         Site(name="理科图书馆", text="自习", effect=[0, -1, 0, 1], isCompulsory=False),
         Site(name="星空咖啡厅", text="消费", effect=[-1, 0, 1, 0], isCompulsory=True),
         Site(name="南区操场", text="锻炼", effect=[0, -1, 1, 0], isCompulsory=False),
         Site(name="管院足球场", text="锻炼", effect=[0, -1, 1, 0], isCompulsory=False),
         Site(name="本部篮球场", text="锻炼", effect=[0, -1, 1, 0], isCompulsory=False),
         Site(name="北区体育馆", text="锻炼", effect=[0, -1, 1, 0], isCompulsory=False),
         Site(name="同济游泳馆", text="游泳", effect=[0, -1, 1, 0], isCompulsory=False),
         Site(name="宿舍", text="休息", effect=[0, -1, 1, 0], isCompulsory=False),
         Site(name="佩琳院", text="保健并报销当年度大学生医保", effect=[1, -1, 1, 0], isCompulsory=False),
         Site(name="光华公司", text="勤工助学", effect=[0, -1, 1, 0], isCompulsory=False),
         Site(name="管理学院史带楼", text="参加调研", effect=[0, -1, 1, 0], isCompulsory=False),
         Site(name="农业银行", text="物价补贴，+41.5", effect=[0, -1, 1, 0], isCompulsory=False),
         Site(name="旦苑小卖部", text="买双皮奶", effect=[0, -1, 1, 0], isCompulsory=False),
         Site(name="五角场", text="吃喝玩乐", effect=[0, -1, 1, 0], isCompulsory=False),
         ]

chances = [{"name": "期中退课", "text": "太菜了", "effect": [-1, 0, 0, 0], "isCompulsory": True},
           {"name": "阿康的诱惑", "text": "冲动消费", "effect": [-1, 0, 0, 0], "isCompulsory": True},
           {"name": "靠一点点续命", "text": "乌龙奶茶加波霸，去冰，三分甜。（私货推荐）", "effect": [-1, 0, 0, 0], "isCompulsory": True}
           {"name": "一卡通丢失", "text": "需要补办一卡通", "effect": [-1, 0, 0, 0], "isCompulsory": True},
           {"name": "自行车损坏", "text": "大一买的这辆自行车，只剩下车架子还是原来的模样。\
           修车的钱，大约是能够再买一辆了吧", "effect": [-1, 0, 0, 0], "isCompulsory": True},
           {"name": "赖床起不来", "text": "早锻刷不完了", "effect": [0, 0, -1, 0], "isCompulsory": True},
           {"name": "三教久留", "text": "熬夜伤肝", "effect": [0, 0, -1, 0], "isCompulsory": True},
           {"name": "我爱学习", "text": "期末努力复习", "effect": [0, 0, 0, 1], "isCompulsory": True},
           {"name": "夸夸群被夸", "text": "斗志昂扬", "effect": [0, 0, 1, 0], "isCompulsory": True},
           ]

initialSizes = []
sizesWithFinalExam = []
initialLocations = [[10, 10]]  # 设计好的位置
locationsWithFinalExam = []
initialLattices = sites   # 设计好的格子
latticesWithFinalExam = sites
remainedChances = chances

contents = {"initialSizes": initialSizes,
            "sizesWithFinalExam": sizesWithFinalExam,
            "initialLocations": initialLocations,
            "LocationsWithFinalExam": locationsWithFinalExam,
            "initialLattices": initialLattices,
            "latticesWithFinalExam": latticesWithFinalExam,
            "chances": chances,
            "remainedChances": remainedChances,
            "grades": grades,
            }

pickle.dump(contents, open('handout/materials/gameContents.data', 'wb'))
