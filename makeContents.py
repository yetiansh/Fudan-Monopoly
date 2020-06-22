import pickle

from handout.classes import *

#   金钱、时间、体力、知识

grades = ['大一', '大二', '大三', '大四']
sites = [Site(name="起点", effect=[0, 0, 0, 0], icon='qidian.png'),
         Site(name="宿舍", action="休息", text="休息", effect=[0, -1, 1, 0], icon='sushe.png', isCompulsory=False),
         Site(name="三教", action="上课", text="听课", effect=[0, -1, 0, 1], icon='sanjiao.png', isCompulsory=False),
         Site(name="光华楼", action="听讲座", text="听讲座", effect=[0, -1, 0, 1], icon='guanghualou.png', isCompulsory=False),
         Site(name="二教", action="上课", text="听课, 优越的地理位置(临近本超和全家)保证了课间总有充足的食物补给", effect=[0, -1, 0, 1],
              icon='erjiao.png',
              isCompulsory=False),
         Site(name="正大体育馆", action="运动", text="", effect=[0, -1, 1, 0], icon='zhengdatiyuguan.png', isCompulsory=False),
         Site(name="本篮", action="打篮球", text="在复旦之光打过球的场地上打球, 我==复旦之光?", effect=[0, -1, 1, 0], icon='benlan.png',
              isCompulsory=False),
         Site(name="佩琳院", action="检查身体", text="保健并报销当年度大学生医保", effect=[1, -1, 1, 0], icon='peilinyuan.png',
              isCompulsory=False),
         Site(name="光华楼小圆桌", action="自习", text="自习", effect=[0, -1, 0, 1], icon='guanghualouxiaoyuanzhuo.png',
              isCompulsory=False),
         Site(name="星空咖啡厅", action="喝咖啡", text="消费", effect=[-1, 0, 1, 0], icon='xingkongkafeiting.png',
              isCompulsory=True),
         Site(name="五教", action="上课", text="在五教自习最快乐的事, 就是带有滑轮的椅子, 可以自由滑动, 坐着很舒适", effect=[0, -1, 0, 1],
              icon='wujiao.png',
              isCompulsory=False),
         Site(name="菜地", action="踢足球", text="有的场地踢足球费鞋, 但这一片就有些特别了, 费洗衣机", effect=[0, -1, 1, 0], icon='caidi.png',
              isCompulsory=False),
         Site(name="农业银行", action="转账", text="物价补贴, +41.5", effect=[0, -1, 1, 0], icon='nongyeyinhang.png',
              isCompulsory=False),
         Site(name="六教", action="上课", text="自习", effect=[0, -1, 0, 1], icon='liujiao.png', isCompulsory=False),
         Site(name="理图", action="借书和自习", text="理科图书馆晚上十点敲响赶人的钟声\n一批人会走向三教\n而我则会走回宿舍", effect=[0, -1, 0, 1],
              icon='litu.png',
              isCompulsory=False),
         Site(name="物理楼", action="做实验", text="我的电压表终于接完了, 到通电的回合了! 测试! 咦, 这股焦香是?!", effect=[0, -1, 0, 1],
              icon='wulilou.png',
              isCompulsory=False),
         Site(name="旦苑", action="买双皮奶", text="双皮奶, 3.8一杯, 午饭后来上一杯, 带给你一下午的快乐", effect=[0, -1, 1, 0], icon='danyuan.png',
              isCompulsory=False),
         Site(name="相辉堂", action="", text="", effect=[0, -1, 0, 0], icon='xianghuitang.png', isCompulsory=False),
         Site(name="五角场", action="娱乐", text="万达百联, 火锅电影, 吃喝玩乐, 带来快乐", effect=[0, -1, 1, 0], icon='wujiaochang.png',
              isCompulsory=False),
         Site(name="书呆子", action="买书", text="买书, 这么便宜的教材和小说\n买不了吃亏买不了上当\n买一本赚一本啊", effect=[-1, 0, 0, 1],
              icon='shudaizi.png',
              isCompulsory=False),
         Site(name="光华公司", action="打工", text="这每小时21.5的工资\n就是我每周还有钱吃饭的基础", effect=[0, -1, 1, 0],
              icon='guanghuagongsi.png', isCompulsory=False),
         Site(name="南操", action="刷锻", text="锻炼", effect=[0, -1, 1, 0], icon='nancao.png', isCompulsory=False),
         Site(name="管院楼", action="参加调研", text="看到这些邀请我去调研的问卷时\n我就知道收入来了", effect=[0, -1, 1, 0],
              icon='guanyuanlou.png',
              isCompulsory=False),
         Site(name="同济游泳馆", action="游泳", text="游泳", effect=[0, -1, 1, 0], icon='tongjiyouyongguan.png',
              isCompulsory=False),
         Site(name="期末考试")
         ]

chances = [{"name": "期中退课", "text": "太菜了, 期中退的课, 选课犯的罪, -130*n", "effect": [-1, 0, 0, 0], "isCompulsory": True},
           {"name": "阿康的诱惑", "text": "上课归来, 饥肠辘辘, 远处飘来烧烤的香气", "effect": [-1, 0, 0, 0], "isCompulsory": True},
           {"name": "靠一点点续命", "text": "乌龙奶茶加波霸, 去冰, 三分甜, 私货推荐", "effect": [-1, 0, 0, 0], "isCompulsory": True},
           {"name": "一卡通丢失", "text": "需要补办一卡通, 复旦信息办收入+20, 每次都在手掌心感受着新鲜出炉的一卡通特有的温热时, \
           收到了一封邮件:\"同学, 我捡到了你的一卡通\"", "effect": [-1, 0, 0, 0], "isCompulsory": True},
           {"name": "自行车损坏", "text": "大一买的这辆自行车, 只剩下车架子还是原来的模样, 修车的钱, 大约是能够再买一辆了吧", "effect": [-1, 0, 0, 0],
            "isCompulsory": True},
           {"name": "赖床起不来", "text": "早锻刷不完了", "effect": [0, 0, -1, 0], "isCompulsory": True},
           {"name": "三教久留", "text": "熬夜伤肝, 不熬伤绩", "effect": [0, 0, -1, 0], "isCompulsory": True},
           {"name": "我爱学习", "text": "期末努力复习", "effect": [0, 0, 0, 1], "isCompulsory": True},
           {"name": "夸夸群被夸", "text": "斗志昂扬", "effect": [0, 0, 1, 0], "isCompulsory": True},
           ]

initialSizes = [[0.136364, 0.1875]] + [[0.090909, 0.1875]] * 8 + [[0.136364, 0.1875]] + [[0.136364, 0.125]] * 5 + \
               [[0.136364, 0.1875]] + [[0.090909, 0.1875]] * 8 + [[0.136364, 0.1875]] + [[0.136364, 0.125]] * 5
sizesWithFinalExam = initialSizes
initialLocations = [[0.863636, 0.8125],
                    [0.772727, 0.8125],
                    [0.681818, 0.8125],
                    [0.590909, 0.8125],
                    [0.5, 0.8125],
                    [0.409091, 0.8125],
                    [0.31818, 0.8125],
                    [0.22727, 0.8125],
                    [0.136364, 0.8125],
                    [0, 0.8125],
                    [0, 0.6875],
                    [0, 0.5625],
                    [0, 0.4375],
                    [0, 0.3125],
                    [0, 0.1875],
                    [0, 0],
                    [0.136364, 0],
                    [0.22727, 0],
                    [0.31818, 0],
                    [0.409091, 0],
                    [0.5, 0],
                    [0.590909, 0],
                    [0.681818, 0],
                    [0.772727, 0],
                    [0.863636, 0],
                    [0.863636, 0.1875],
                    [0.863636, 0.3125],
                    [0.863636, 0.4375],
                    [0.863636, 0.5625],
                    [0.863636, 0.6875]]
locationsWithFinalExam = initialLocations
initialLattices = sites[0:3] + [Chance(name="命运", icon='mingyun1.png')] + sites[3:6] + \
                  [Chance(name="挑战", icon='tiaozhan2.png')] + sites[6:11] + \
                  [Chance(name="命运", icon='mingyun2.png')] + sites[11:15] + \
                  [Chance(name="命运", icon='mingyun.png')] + sites[15:18] + \
                  [Chance(name="挑战", icon='tiaozhan.png')] + sites[18:23] +\
                  [Chance(name="挑战", icon='tiaozhan1.png')] + sites[23:24]
latticesWithFinalExam = initialLattices
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

pickle.dump(contents, open('handout/materials/gameContents.dat', 'wb'))
