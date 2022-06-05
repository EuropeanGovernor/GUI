import random
import sys,math
import re
import numpy as np
import sqlite3
import pyqtgraph as pg
from pyqtgraph import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets,QtGui,QtSql
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FC
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QVBoxLayout, QWidget
import datetime
import urllib.request
import gzip
import json
import borax
from borax.calendars.festivals2 import FestivalLibrary

import selenium
import Get_Daily_Menu
import Recommend_Dishes
import s
plt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置字体
plt.rcParams["axes.unicode_minus"] = False  # 该语句解决图像中的“-”负号的乱码问题
class MyQLabel(QLabel):
    DoubleClicked = pyqtSignal()
    def __int__(self):
        super().__init__()
    def mouseDoubleClickEvent(self, e):
        self.DoubleClicked.emit()
class Mainui(QMainWindow,QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        tb=self.addToolBar('')
        tool1=QAction(QIcon('.\\recipe.png'),'历史菜谱',self)
        tool2 = QAction(QIcon('.\\statistic.png'), '个人数据', self)
        tool3 = QAction(QIcon('.\\weight.png'), '更新体重', self)
        tool4 =QAction(QIcon('.\\height.png'), '更新身高', self)
        tool5 = QAction(QIcon('.\\illness.png'), '添加状态', self)
        tool6 = QAction(QIcon('.\\meal.png'), '记录', self)
        tool7 = QAction(QIcon('.\\news.png'), '评估', self)

        tb.addAction(tool1)
        tb.addAction(tool7)
        tb.addAction(tool2)
        tb.addAction(tool3)
        tb.addAction(tool4)
        tb.addAction(tool5)
        tb.addAction(tool6)

        tool1.triggered.connect(self.history)
        tool2.triggered.connect(self.statistic)
        tool3.triggered.connect(self.weight)
        tool4.triggered.connect(self.height)
        tool5.triggered.connect(self.status)
        tool6.triggered.connect(self.meal)
        tool7.triggered.connect(self.assess)

        # self.desktop = QApplication.desktop()
        # # 获取显示器分辨率大小
        # self.screenRect = self.desktop.screenGeometry()
        # self.height =self.screenRect.height()/1440
        # self.width = self.screenRect.width()/2160

        self.main_widget = QtWidgets.QWidget()
        self.label = QtWidgets.QLabel(self.main_widget)
        png = QPixmap()
        png.load("./3.jpg")
        self.label.setPixmap(png)
        self.label.resize(2000,1236)
        self.setCentralWidget(self.main_widget)

        label1 = QLabel(self)
        label1.setGeometry(0, 0, 1000, 300)  # 设置标签的大小,标签不能出主窗口，所以move时候要注意
        label1.setText('<font style="font-family:方正舒体" style="font-size:150px" color=black>健康食谱</font>')
        label1.move(930, 80)

        label2 = QLabel(self)
        label2.setGeometry(0, 0, 1000, 300)  # 设置标签的大小,标签不能出主窗口，所以move时候要注意
        label2.setText('<font style="font-family:方正舒体" style="font-size:60px" color=black>为您推荐：</font>')
        label2.move(1120, 230)

        self.label4 = QLabel(self)  # 天气
        self.get_weather_data()

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        boy=MyQLabel(self)
        boys=QPixmap()
        boys.load("./boy.png")
        boy.setPixmap(boys)
        boy.resize(100,100)
        boy.setToolTip('我是男生')
        boy.DoubleClicked.connect(self.M)
        boy.move(1800, 1110)

        girl = MyQLabel(self)
        girls = QPixmap()
        girls.load("./girl.png")
        girl.setPixmap(girls)
        girl.resize(100,100)
        girl.setToolTip('我是女生')
        girl.DoubleClicked.connect(self.F)
        girl.move(1900, 1110)

        self.label3 = QLabel(self)#刷新
        refresh=MyQLabel(self)
        refreshs=QPixmap()
        refreshs.load('./refresh.png')
        refresh.setPixmap(refreshs)
        refresh.resize(100,100)
        refresh.setToolTip('刷新')
        refresh.DoubleClicked.connect(self.ref)
        refresh.move(1400, 340)

        urls=['http://mp.weixin.qq.com/s?__biz=MzU4NzI3ODUyNA==&mid=2247504342&idx=2&sn=f6cd0d421badc032bc02581a1cf38c97&chksm=fdece005ca9b6913a54e2fbfac188ced7ced6e6404a87bfdfa8e51c5fc019e0bdb36c0cb7d8e#rd',
              'http://mp.weixin.qq.com/s?__biz=MzU4NzI3ODUyNA==&mid=2247504317&idx=2&sn=b710640e75bf01f3203de2dba2c6ac3c&chksm=fdece06eca9b697804febd73579f5a4858affe3835aeff76eaa15fa1638be64e765c1d454eae#rd',
              'http://mp.weixin.qq.com/s?__biz=MzU4NzI3ODUyNA==&mid=2247504298&idx=2&sn=29f6f1efe7c94915a31ea8980a1bdaaf&chksm=fdece079ca9b696f9e244a359a4dcda9bbfac3bfd0b47bb49597db4c4460490477f6f1046e64#rd',
              'http://mp.weixin.qq.com/s?__biz=MzU4NzI3ODUyNA==&mid=2247504279&idx=2&sn=53b0ddc7e683f573ed0233e63e35b9c4&chksm=fdece044ca9b69529d00f8ed38195fcc56d3290cd8171341ae3f379ba360558f79de35e44e87#rd',
              'http://mp.weixin.qq.com/s?__biz=MzU4NzI3ODUyNA==&mid=2247504255&idx=2&sn=8ea11f4978b87365590c0ff8520830f8&chksm=fdece0acca9b69bac71480e745c2a73998d970cbd14b4656685cf7d4c99a46932eec2fe8b787#rd',
              'http://mp.weixin.qq.com/s?__biz=MzU4NzI3ODUyNA==&mid=2247504236&idx=2&sn=1a3529417642199b72f198f79ff6734f&chksm=fdece0bfca9b69a9d3fadb37e6f1040ebc9abdd10f2b50051862ade754724a7717966664abc9#rd',
              'http://mp.weixin.qq.com/s?__biz=MzU4NzI3ODUyNA==&mid=2247504219&idx=2&sn=2c4d3617029f0980f86382181140a9c2&chksm=fdece088ca9b699e9b5c776e2f269ed80e21752a51e7bcb14c702716c64445e069d11d0a4bcb#rd']
        Get_Daily_Menu.process_Url(urls[datetime.datetime.now().day//7])

        self.child_window = Child()
        self.child_window2=Child2()
        self.setWindowTitle('健康食谱')
        self.setFixedSize(2000,1236)
        self.center()
    def assess(self):
        self.child_window2.show()
    def ref(self):
        if datetime.datetime.now().hour<=15:
            temp = Recommend_Dishes.Recommend_lunch()
        else:
            temp = Recommend_Dishes.Recommend_supper()
        text = ''
        for i in range(len(temp)):
            r = temp[i].split('*')
            print(r)
            text += f'{r[0]}'.ljust(10, '…')
            text += f'{r[1]}\n\n'
        self.label3.setGeometry(0, 0, 1000, 600)
        self.label3.setStyleSheet("QLabel{color:purple;font-size:45px;font-family:'方正舒体';}")
        self.label3.setText(text)
        self.label3.setWordWrap(True)
        self.label3.move(1020, 410)
    def M(self):
        con = sqlite3.connect('.\db.db')
        cur = con.cursor()
        sql = 'UPDATE sex set sex=?'
        cur.execute(sql, 'M')
        con.commit()
        self.statusBar.showMessage("更新成功！", 3000)
        cur.close()
        con.close()
    def F(self):
        con = sqlite3.connect('.\db.db')
        cur = con.cursor()
        sql = 'UPDATE sex set sex=?'
        cur.execute(sql, 'F')
        con.commit()
        self.statusBar.showMessage("更新成功！", 3000)
        cur.close()
        con.close()
    def history(self):
        dialog = QDialog()
        dialog.setWindowTitle('历史菜单')
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.setFixedSize(1600, 900)
        min=QDate.currentDate().addDays(-15).toString(Qt.DefaultLocaleLongDate)
        max=QDate.currentDate().addDays(0).toString(Qt.DefaultLocaleLongDate)
        std=re.compile('\d+')
        result0=std.findall(min)
        result1=std.findall(max)
        self.cal=QCalendarWidget(dialog)
        self.cal.setMinimumDate(QDate(int(result0[0]),int(result0[1]),int(result0[2])))
        self.cal.setMaximumDate(QDate(int(result1[0]),int(result1[1]),int(result1[2])))
        self.cal.resize(750,900)
        self.cal.setGridVisible(True)
        pic = QLabel(dialog)
        png = QPixmap()
        png.load("./menu.jpg")
        pic.resize(950, 900)
        pic.setPixmap(png)
        pic.move(750,0)
        hbox = QHBoxLayout(dialog)
        dialog.setLayout(hbox)
        self.cal.clicked.connect(self.show_date)
        self.label = QLabel(dialog)
        self.label.setGeometry(0, 0, 1000, 930)
        self.label.setStyleSheet("QLabel{color:green;font-size:30px;font-family:'宋体';}")
        self.label.setWordWrap(True)
        self.label.move(1050, -120)
        dialog.exec()
    def get_weather_data(self):
        url1 = 'http://wthrcdn.etouch.cn/weather_mini?city=' + urllib.parse.quote('昌平')
        weather_data = urllib.request.urlopen(url1).read()
        # 读取网页数据
        weather_data = gzip.decompress(weather_data).decode('utf-8')
        # 解压网页数据
        weather_dict = json.loads(weather_data)
        # 将json数据转换为dict数据
        forecast = weather_dict.get('data').get('forecast')
        wendu=weather_dict.get('data').get('wendu')
        # ganmao=weather_dict.get('data').get('ganmao')
        high=forecast[0].get('high').split('高温')
        low=forecast[0].get('low').split('低温')
        type=forecast[0].get('type')

        temp = ''
        library = FestivalLibrary.load_builtin()
        names = library.get_festival_names(datetime.date.today())
        if len(names) > 0:
            temp+=f'今天是{names[0]}\n\n'
        temp+=f'温度：{wendu}℃\n\n'
        # temp+=f'感冒：{ganmao}\n\n'
        temp+=f'高温:{high[1]}\n\n'
        temp+=f'低温:{low[1]}\n\n'
        temp+=f'天气：{type}'
        self.label4.setStyleSheet("QLabel{color:purple;font-size:40px;font-family:'楷体';}")
        self.label4.setWordWrap(True)
        self.label4.setText(temp)
        self.label4.setGeometry(0,0,500,500)
        self.label4.move(50,100)

    def show_date(self):
        self.date = self.cal.selectedDate()
        lists = s.get_history_when(self.date.toString("yyyy-MM-dd"))
        temp = ''
        for i in range(len(lists)):
            a = lists[i].split('*')
            temp += f'{a[0]}'.ljust(10, '…')
            temp += f'{a[1]}\n'
        self.label.setText(temp)
    def statistic(self):
        dialog = QDialog()
        dialog.setWindowTitle('个人数据')
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.resize(1500, 900)

        con= sqlite3.connect(".\db.db")
        cursor = con.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='weight';")
        content = cursor.execute("SELECT date,weight from weight")
        x,y,z=[0],[],[]
        for row in content:
            y.append(float(row[1]))
            z.append(row[0])
        pg.setConfigOptions(antialias=True, foreground=QColor(0, 0, 0))
        xdict = dict(enumerate(z))
        stringaxis = pg.AxisItem(orientation='bottom')
        stringaxis.setTicks([xdict.items()])
        w = pg.PlotWidget(axisItems={'bottom': stringaxis})
        w.plot(list(xdict.keys()),y,pen=pg.mkPen('b'),symbol='o')

        w.showGrid(x=True, y=True)
        w.setTitle('体重变化', color='008080', size='12pt')
        w.setLabel('left', '体重(kg)')
        w.setLabel('bottom', '时间')
        w.setBackground('w')

        cursor.execute("SELECT name FROM sqlite_master WHERE type='height';")
        content = cursor.execute("SELECT date,height from height")
        a,b,c = [0], [], []
        for row in content:
            b.append(float(row[1]))
            c.append(row[0])
        adict = dict(enumerate(c))
        stringaxish = pg.AxisItem(orientation='bottom')
        stringaxish.setTicks([adict.items()])
        h = pg.PlotWidget(axisItems={'bottom': stringaxish})
        h.plot(list(adict.keys()),b,pen=pg.mkPen('b'),symbol='o')

        h.showGrid(x=True, y=True)
        h.setTitle('身高变化', color='008080', size='12pt')
        h.setLabel('left', '身高(cm)')
        h.setLabel('bottom', '时间')
        h.setBackground('w')
        cursor.close()
        con.close()

        vbox=QVBoxLayout(dialog)
        vbox.addWidget(w)
        vbox.addWidget(h)
        dialog.setLayout(vbox)
        dialog.exec()
    def weight(self):
        num,ok = QInputDialog.getDouble(self, '更新体重(kg)','听说坚持记录体重会变瘦！',min=0)
        if ok:
            con = sqlite3.connect('.\db.db')
            cur = con.cursor()
            sql = 'insert into weight(date,weight) values(?,?)'
            current_date = QDate.currentDate().toString('yyyy-MM-dd')
            temp=(current_date,num)
            cur.execute(sql,temp)
            con.commit()
            self.statusBar.showMessage("记录成功！",3000)
            cur.close()
            con.close()
    def height(self):
        num, ok = QInputDialog.getDouble(self, '更新身高(cm)', '大学也有机会长高！', min=0)
        if ok:
            con = sqlite3.connect('.\db.db')
            cur = con.cursor()
            sql = 'insert into height(date,height) values(?,?)'
            current_date = QDate.currentDate().toString('yyyy-MM-dd')
            temp = (current_date, num)
            cur.execute(sql, temp)
            con.commit()
            self.statusBar.showMessage("记录成功！",3000)
            cur.close()
            con.close()
    def status(self):
        dialog = QDialog()
        dialog.setWindowTitle('添加状态')
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.setFixedSize(1000,618)

        toothache=QLabel(dialog)
        menstrual_cycle = QLabel(dialog)
        allergic= QLabel(dialog)
        headache = QLabel(dialog)
        stomachache= QLabel(dialog)
        healthy=QLabel(dialog)

        toothache.setText('<a href="https://dxy.com/article/320"><img src=".\\toothache.png"></a>')
        menstrual_cycle.setText('<a href="https://dxy.com/article/3040"><img src=".\\menstrual-cycle.png"></a>')
        allergic.setText('<a href="https://dxy.com/article/3851"><img src=".\\allergic.png"></a>')
        headache.setText('<a href="https://dxy.com/article/7722"><img src=".\\headache.png"></a>')
        stomachache.setText('<a href="https://dxy.com/article/5622"><img src=".\\stomachache.png"></a>')
        healthy.setText('<a href="https://dxy.com/articles/24834"><img src=".\\healthy.png"></a>')

        toothache.linkActivated.connect(self.trans_status)
        menstrual_cycle.linkActivated.connect(self.trans_status)
        headache.linkActivated.connect(self.trans_status)
        allergic.linkActivated.connect(self.trans_status)
        stomachache.linkActivated.connect(self.trans_status)
        healthy.linkActivated.connect(self.trans_status)

        toothache.setToolTip('牙痛')
        menstrual_cycle.setToolTip('经期')
        allergic.setToolTip('过敏')
        headache.setToolTip('头痛')
        healthy.setToolTip('健康')
        stomachache.setToolTip('胃痛')

        grid=QGridLayout(dialog)
        grid.setSpacing(100)
        grid.setAlignment(Qt.AlignCenter)
        grid.addWidget(toothache,0,0)
        grid.addWidget(menstrual_cycle, 1, 0)
        grid.addWidget(allergic,0,1)
        grid.addWidget(headache,1,1)
        grid.addWidget(stomachache,0,2)
        grid.addWidget(healthy,1,2)
        dialog.setLayout(grid)
        dialog.exec()
    def trans_status(self):
        sender = self.sender()
        t=sender.text()

        con = sqlite3.connect('.\db.db')
        cur = con.cursor()
        current_date = QDate.currentDate().toString('yyyy-MM-dd')
        sql1 = 'UPDATE status set date=?'
        cur.execute(sql1, [current_date])
        sql2 = 'UPDATE status set name=?'
        if 'toothache' in t:
            url=['https://dxy.com/article/2488','https://dxy.com/article/9460',"https://dxy.com/article/320"]
            QDesktopServices.openUrl(QUrl(url[random.randint(0, 3)]))
            cur.execute(sql2, ['牙痛'])
        elif 'allergic' in t:
            url=['https://dxy.com/article/5847','https://dxy.com/article/2627',"https://dxy.com/article/3851"]
            QDesktopServices.openUrl(QUrl(url[random.randint(0, 3)]))
            cur.execute(sql2, ['过敏'])
        elif 'menstrual' in t:
            url=['https://dxy.com/article/16823',"https://dxy.com/article/3040",'https://dxy.com/article/79314']
            QDesktopServices.openUrl(QUrl(url[random.randint(0, 3)]))
            cur.execute(sql2, ['生理期'])
        elif 'headache' in t:
            url=['https://dxy.com/article/6879',"https://dxy.com/article/7722",'https://dxy.com/article/6253']
            QDesktopServices.openUrl(QUrl(url[random.randint(0, 3)]))
            cur.execute(sql2, ['头痛'])
        elif 'stomachache' in t:
            url=['https://dxy.com/article/3684',"https://dxy.com/article/5622",'https://dxy.com/article/16347']
            QDesktopServices.openUrl(QUrl(url[random.randint(0, 3)]))
            cur.execute(sql2,['胃痛'])
        elif 'healthy' in t:
            url=['https://dxy.com/baike/category/24834?tag_id=0',"https://dxy.com/baike/category/24838?tag_id=0",
                 'https://dxy.com/baike/category/24836?tag_id=0','https://dxy.com/baike/category/24840?tag_id=0']
            QDesktopServices.openUrl(QUrl(url[random.randint(0, 4)]))
            cur.execute(sql2, ['健康'])

        self.statusBar.showMessage("记录状态成功！", 3000)
        con.commit()
        cur.close()
        con.close()
    def meal(self):
        self.child_window.show()
    def center(self):
        #将这个控件(QWidget)的几何内容(宽高位置等)，赋值给qr
        qr = self.frameGeometry()
        #计算出显示器的屏幕分辨率，得到中心点
        cp = QDesktopWidget().availableGeometry().center()
        #移动
        qr.moveCenter(cp)
        self.move(qr.topLeft())
class Child2(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("记录")
        self.resize(1500,927 )
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.addTab(self.tab1, 'Tab1')
        self.addTab(self.tab2, 'Tab2')
        self.tab1UI()
        self.tab2UI()
    def tab1UI(self):
        self.setTabText(0, "统计")
        self.fig = plt.Figure()
        self.canvas = FC(self.fig)
        self.slot_btn_start()
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.tab1.setLayout(layout)
    def slot_btn_start(self):
        ax = self.fig.add_subplot(111)
        x = ['脂肪', '蛋白质', '碳水','VA','VB6','VC','钙','铁','锌','膳食纤维','热量','推荐量']
        y=s.week_assess()[0]
        y.append(1)
        ax.cla()
        ax.barh(x, y)
        ax.title.set_text('上周摄入达推荐值：')
        ax.title.set_size(30)
        ax.set_yticks(x)  # 使用axis.set_xticks固定刻度位置   (新添加内容)
        ax.set_yticklabels(x)  # 将时间戳作为x轴标签
        ax.set_yticklabels(x,fontsize=20)
        ax.tick_params(axis='x',labelsize=20)
        self.canvas.draw()
    def tab2UI(self):
        self.setTabText(1, "建议")
        pic = QLabel(self.tab2)
        png = QPixmap()
        png.load("./1.jpg")
        pic.resize(1500, 927)
        pic.setPixmap(png)
        hbox=QHBoxLayout(self.tab2)
        label = QLabel(self.tab2)
        label.setGeometry(100, 100, 1300, 827)
        label.setStyleSheet("QLabel{color:black;font-size:30px;font-family:'楷体';}")
        label.setText(s.week_assess()[1])
        label.setWordWrap(True)
        self.tab2.setLayout(hbox)
class Child(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("记录")
        self.resize(1000,650)
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab5 = QWidget()
        self.addTab(self.tab1, 'Tab1')
        self.addTab(self.tab2, 'Tab2')
        self.addTab(self.tab3, 'Tab3')
        self.addTab(self.tab4, 'Tab4')
        self.addTab(self.tab5, 'Tab5')
        self.tab1UI()
        self.tab2UI()
        self.tab3UI()
        self.tab4UI()
        self.tab5UI()
    def tab1UI(self):
        self.setTabText(0, "统计")
        self.fig = plt.Figure()
        self.canvas = FC(self.fig)
        self.slot_btn_start()
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.tab1.setLayout(layout)

    #接口
    def slot_btn_start(self):
        con = sqlite3.connect(".\db.db")
        cursor = con.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='history';")
        content = cursor.execute("SELECT date,nutrition from history")
        for row in content:
            if row[0]==QDate.currentDate().toString('yyyy-MM-dd'):
                temp=row[1].split(':')
                data=[temp[10],temp[1],temp[0],temp[2]]
            else:
                data=[0,0,0,0]
        ax = self.fig.add_subplot(111)
        x = ['热量',  '蛋白质', '脂肪','碳水','推荐量']
        rule=s.get_weekstandard()
        y=[float(data[0])/rule[10],float(data[1])/rule[0],float(data[2])/rule[1],float(data[3])/rule[2],1]
        ax.cla()
        ax.barh(x, y)
        ax.title.set_text('今日摄入达推荐值：')
        ax.title.set_size(30)
        ax.set_yticks(x)  # 使用axis.set_xticks固定刻度位置   (新添加内容)
        ax.set_yticklabels(x)  # 将时间戳作为x轴标签
        ax.set_yticklabels(x, fontsize=20)
        ax.tick_params(axis='x', labelsize=20)
        self.canvas.draw()
        cursor.close()
        con.close()

    def doubleClickedHandle(self, index):
        num,ok= QInputDialog.getDouble(self, '记录', '请输入份数：', min=0)
        print(num)

    def tab2UI(self):
        e= DataGrid('today_menu')
        hbox = QHBoxLayout()
        hbox.addWidget(e)
        self.tab2.setLayout(hbox)
        self.setTabText(1, "早餐")

    def tab3UI(self):
        e = DataGrid('today_menu')
        hbox = QHBoxLayout()
        hbox.addWidget(e)
        self.tab3.setLayout(hbox)
        self.setTabText(2, "午餐")


    def tab4UI(self):
        e = DataGrid('today_menu')
        hbox = QHBoxLayout()
        hbox.addWidget(e)
        self.tab4.setLayout(hbox)
        self.setTabText(3, "晚餐")


    def tab5UI(self):
        e = DataGrid('snacks')
        hbox = QHBoxLayout()
        hbox.addWidget(e)
        self.tab5.setLayout(hbox)
        self.setTabText(4, "加餐")
class DataGrid(QWidget):
    def createTableAndInit(self):
        # 添加数据库
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        # 设置数据库名称
        self.db.setDatabaseName('./db.db')
        self.db.open()
        return True
    def __init__(self,mode):
        super().__init__()
        self.mode=mode
        self.createTableAndInit()
        # 当前页
        self.currentPage = 0
        # 总页数
        self.totalPage = 0
        # 总记录数
        self.totalRecrodCount = 0
        # 每页显示记录数
        self.PageRecordCount = 10
        self.initUI()
    def initUI(self):
        # 创建窗口
        self.createWindow()
        # 设置表格
        self.setTableView()
        # 信号槽连接
        self.prevButton.clicked.connect(self.onPrevButtonClick)
        self.nextButton.clicked.connect(self.onNextButtonClick)
    def closeEvent(self, event):
        # 关闭数据库
        self.db.close()
    # 创建窗口
    def createWindow(self):
        # 操作布局
        operatorLayout = QHBoxLayout()
        self.prevButton = QPushButton("前一页")
        self.nextButton = QPushButton("后一页")
        operatorLayout.addWidget(self.prevButton)
        operatorLayout.addWidget(self.nextButton)
        # 状态布局
        statusLayout = QHBoxLayout()
        self.totalPageLabel = QLabel()
        self.totalPageLabel.setFixedWidth(100)
        self.currentPageLabel = QLabel()
        self.currentPageLabel.setFixedWidth(100)

        self.totalRecordLabel = QLabel()
        self.totalRecordLabel.setFixedWidth(100)

        statusLayout.addWidget(self.totalPageLabel)
        statusLayout.addWidget(self.currentPageLabel)
        statusLayout.addWidget(QSplitter())
        statusLayout.addWidget(self.totalRecordLabel)

        # 设置表格属性
        self.tableView = QTableView()
        # 表格宽度的自适应调整
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 创建界面
        mainLayout = QVBoxLayout(self);
        mainLayout.addLayout(operatorLayout);
        mainLayout.addWidget(self.tableView);
        mainLayout.addLayout(statusLayout);
        self.setLayout(mainLayout)
    # 设置表格
    def setTableView(self):
        # 声明查询模型
        self.queryModel = QSqlQueryModel(self)
        # 设置当前页
        self.currentPage = 1;
        # 得到总记录数
        self.totalRecrodCount = self.getTotalRecordCount()
        # 得到总页数
        self.totalPage = self.getPageCount()
        # 刷新状态
        self.updateStatus()
        # 设置总页数文本
        self.setTotalPageLabel()
        # 设置总记录数
        self.setTotalRecordLabel()
        # 记录查询
        self.recordQuery(0)
        # 设置模型
        self.tableView.setModel(self.queryModel)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setStyleSheet("alternate-background-color: rgb(0, 255, 127)"
                                     "; background-color: rgb(244, 244, 244);")
        # 设置表格表头
        self.queryModel.setHeaderData(0, Qt.Horizontal, "名称")
        self.tableView.doubleClicked.connect(self.doubleClickedHandle)
    #接口
    def doubleClickedHandle(self, index):
        num, ok = QInputDialog.getDouble(self, '记录', '请输入份数：', min=0)
        if num>0:
            con = sqlite3.connect('.\db.db')
            cursor = con.cursor()
            sql = f"select menu from {self.mode}" if self.mode=='today_menu' else "select id from snacks"
            results = cursor.execute(sql).fetchall()
            s.add2_todayselect(results[10*(self.currentPage-1)+index.row()][0],num)
    # 得到记录数
    def getTotalRecordCount(self):
        self.queryModel.setQuery(f"select * from {self.mode}")
        rowCount = self.queryModel.rowCount()
        return rowCount
    # 得到页数
    def getPageCount(self):
        if self.totalRecrodCount % self.PageRecordCount == 0:
            return (self.totalRecrodCount / self.PageRecordCount)
        else:
            return (self.totalRecrodCount //self.PageRecordCount + 1)
    # 记录查询
    def recordQuery(self, limitIndex):
        a,b=limitIndex, self.PageRecordCount
        szQuery = (f"select * from {self.mode} limit {a},{b}" )
        self.queryModel.setQuery(szQuery)
    # 刷新状态
    def updateStatus(self):
        szCurrentText = ("当前第%d页" % self.currentPage)
        self.currentPageLabel.setText(szCurrentText)
        # 设置按钮是否可用
        if self.currentPage == 1:
            self.prevButton.setEnabled(False)
            self.nextButton.setEnabled(True)
        elif self.currentPage == self.totalPage:
            self.prevButton.setEnabled(True)
            self.nextButton.setEnabled(False)
        else:
            self.prevButton.setEnabled(True)
            self.nextButton.setEnabled(True)
    # 设置总数页文本
    def setTotalPageLabel(self):
        szPageCountText = ("总共%d页" % self.totalPage)
        self.totalPageLabel.setText(szPageCountText)
    # 设置总记录数
    def setTotalRecordLabel(self):
        szTotalRecordText = ("共%d条" % self.totalRecrodCount)
        self.totalRecordLabel.setText(szTotalRecordText)
    # 前一页按钮按下
    def onPrevButtonClick(self):
        limitIndex = (self.currentPage - 2) * self.PageRecordCount
        self.recordQuery(limitIndex)
        self.currentPage -= 1
        self.updateStatus()
    # 后一页按钮按下
    def onNextButtonClick(self):
        limitIndex = self.currentPage * self.PageRecordCount
        self.recordQuery(limitIndex)
        self.currentPage += 1
        self.updateStatus()
if __name__ == '__main__':
    app=QApplication(sys.argv)
    app.setWindowIcon(QIcon('.\\nutrition.svg'))
    GUI=Mainui()
    GUI.show()
    sys.exit(app.exec_())