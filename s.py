import sqlite3
import datetime
def get_nutrition(name):##查询菜品是否存在，存在则返回营养信息
    con=sqlite3.connect('db.db')
    cursor_obj=con.cursor()
    if len(name)==1:
        nutrition = []
        cursor_obj.execute('SELECT * FROM meals WHERE id=?',(name[0],))
        a=cursor_obj.fetchall()
        if not a:
            cursor_obj.execute('SELECT * FROM snacks WHERE id=?', (name[0],))
            a = cursor_obj.fetchall()
        if a:
            a = a[0]
            for i in range(11):
                nutrition.append(str(a[i+1]))
            nutrition=':'.join(nutrition)
        else:nutrition=''
    else:
        nutrition=[0]*11
        for n in name:
            cursor_obj.execute('SELECT * FROM meals WHERE id=?', (n,))
            a = cursor_obj.fetchall()
            if not a:
                cursor_obj.execute('SELECT * FROM snacks WHERE id=?', (name[0],))
                a = cursor_obj.fetchall()
            if a:
                a = a[0]
                for i in range(11):
                    nutrition[i]+=a[i+1]
        nutrition=[str(i) for i in nutrition]
        nutrition=':'.join(nutrition)
    return nutrition

# print(get_nutrition(['煮鸡蛋','小米粥','土豆牛肉']))
##输入的是菜名列表，查询菜品是否存在支持一个一个查询。例如['馒头']；计算总营养则列表可以包含多个菜名。
##nutrition是字符串，334.0:25.0:45.1:12.3:25.4:22.0:33.0:45.0:1.0:1.0:1.0
###蛋白质，脂肪，碳水化合物，a,b,c，钙，铁，锌，膳食纤维，热量 11个浮点数用冒号分开
##若菜名不存在，则nutrition为 ''
def get_last_week():
    a=[]
    dlist=[]
    today = datetime.datetime.today()
    days_count = datetime.timedelta(days=today.isoweekday())
    end_time = today - days_count
    a.append(end_time)
    for i in range(6):
        b=datetime.timedelta(days=i+1)
        c=end_time-b
        a.append(c)
    for i in a:
        year = i.strftime("%Y")
        month = i.strftime("%m")
        day = i.strftime("%d")
        s=f"{year}-{month}-{day}"
        dlist.append(s)
    return dlist
def add2_todaymenu(name_list):##清空记录，并添加菜品到当日菜谱
    try:
        con=sqlite3.connect('db.db')
        cursor_obj=con.cursor()
        cursor_obj.execute('DROP TABLE today_menu')
        cursor_obj.execute('CREATE TABLE today_menu'
                           '(menu text)')
        for name in name_list:
            cursor_obj.execute('INSERT INTO today_menu(menu) VALUES(?)',(name,))
        con.commit()
    except:pass
# add2_todaymenu(['黄瓜','放松放松','水电费','个'])
###输入的是菜名字符串列表。比如['馒头','叉烧肉','西红柿炒鸡蛋']

def get_latest_pd():###查询用户最新的身高体重
    con=sqlite3.connect('db.db')
    cursor_obj=con.cursor()
    n1=cursor_obj.execute('SELECT COUNT(*) FROM weight').fetchall()[0][0]
    w=cursor_obj.execute('SELECT weight FROM weight LIMIT 1 OFFSET '+str(n1-1)).fetchall()[0][0]
    n2=cursor_obj.execute('SELECT COUNT(*) FROM height').fetchall()[0][0]
    h=cursor_obj.execute('SELECT height FROM height LIMIT 1 OFFSET '+str(n2-1)).fetchall()[0][0]
    pd_list=[h,w]
    return pd_list
# print(get_latest_pd())
###pd_list是浮点数列表  [173.0,55.0]

def get_selected():###获取当日已选菜品
    name_list=[]
    con=sqlite3.connect('db.db')
    cursor_obj=con.cursor()
    aa=cursor_obj.execute('SELECT name FROM today_select').fetchall()
    for a in aa:
        name_list.append(a[0])
    return name_list
# print(get_selected())
######输出的是菜名字符串列表。比如['馒头','叉烧肉','西红柿炒鸡蛋']

def get_todaymenu():###获取当日菜谱列表
    name_list=[]
    con=sqlite3.connect('db.db')
    cursor_obj=con.cursor()
    aa=cursor_obj.execute('SELECT menu FROM today_menu').fetchall()
    for a in aa:
        name_list.append(a[0])
    return name_list
# print(get_todaymenu())
######输出的是菜名字符串列表。比如['馒头','叉烧肉','西红柿炒鸡蛋']
def get_history_when(date):###根据日期得到历史菜品，输入例如'2021-05-20'
    con=sqlite3.connect('db.db')
    cursor_obj=con.cursor()
    meals=cursor_obj.execute('SELECT meals FROM history WHERE date=?',(date,)).fetchall()
    if meals:meals=meals[0][0].split(',')
    return meals
###meals为字符串列表，例如['馒头*1','米饭*2','香蕉*3']

print(get_history_when('2022-05-25'))
def add2_todayselect(name,p):##将菜品添加到today_select
    try:
        name=name+'*'+str(p)
        con=sqlite3.connect('db.db')
        cursor_obj=con.cursor()
        today=datetime.datetime.today()
        today=today.strftime('%Y')+'-'+today.strftime('%m')+'-'+today.strftime('%d')
        cursor_obj.execute('INSERT INTO today_select(date,name) VALUES(?,?)', (today,name))
        cursor_obj.execute('DELETE FROM history WHERE date=?',(today,))
        aa=cursor_obj.execute('SELECT name FROM today_select WHERE date=?',(today,)).fetchall()
        meals=[]
        for a in aa:
            meals.append(a[0])
        meals=','.join(meals)
        ns=[0]*11
        for a in aa:
            a=a[0]
            vb=float(a.split('*')[-1])
            va=[a.split('*')[0]]
            n=get_nutrition(va)
            n=n.split(':')
            n=[float(i)*vb for i in n]
            for i in range(11):
                ns[i]+=n[i]
        ns=[str(i) for i in ns]
        ns=':'.join(ns)
        cursor_obj.execute('INSERT INTO history(date,meals,nutrition) VALUES(?,?,?)',(today,meals,ns))
        con.commit()
    except:pass
###  输入的name是一个菜名字符串,p是浮点份数
# add2_todayselect('苹果',2.0)
# add2_todayselect('香蕉',3.0)
def week_assess():##周食谱评估
    try:
        con=sqlite3.connect('db.db')
        cursor_obj=con.cursor()
        dlist=get_last_week()
        alist=[]
        nutrition=[0]*11
        weight=get_latest_pd()[1]
        for day in dlist:
            a=cursor_obj.execute('SELECT nutrition FROM history WHERE date=?',(day,)).fetchall()
            if a:
                a=a[0][0].split(':')
                a=[float(i) for i in a]
                alist.append(a)
        for a in alist:
            for i in range(11):
                nutrition[i]+=a[i]
        nutrition=[i*7/len(alist) for i in nutrition]
        criterion=[weight*7,weight*7,weight*35,5000*7,30*7,100*7,1000*7,12.5*7,1.5*7,30*7,weight*280]
    ###正常人一天：蛋白质（1g*weight），脂肪（1g*weight），碳水化合物（5g*weight）
        # 维a(5000国际单位)，维b（1.5mg）,维c（100mg）
        #钙（1000mg）,铁（12.5mg），锌（15mg）
        #膳食纤维（30g），热量（40大卡*weight）
        x=[]
        for i in range(11):
            x.append(float('%.4f'%(nutrition[i]/criterion[i])))
        advice=''
        num=1
        if x[0]<0.75:
            advice+=str(num)+'.'+'您上周蛋白质摄入不足，若不及时调整，可能会导致水肿，身体消瘦，贫血，发育不良等'+'\n'
            num+=1
        if x[0]>1.25:
            advice+=str(num)+'.'+'您上周蛋白质摄入超标，若不及时调整，可能会加重肾脏和肝的负担，痛风，还可能引起泌尿系统结石'+'\n'
            num+=1
        if x[1]<0.75:
            advice+=str(num)+'.'+'您上周脂肪摄入不足，若不及时调整，可能会导致营养不良，肠胃功能下降皮肤受损，维生素D缺乏'+'\n'
            num+=1
        if x[1]>1.25:
            advice+=str(num)+'.'+'您上周脂肪摄入超标，若不及时调整，可能会增加肠胃负担，导致身体肥胖，高血脂高血压，脂肪肝等'+'\n'
            num+=1
        if x[2]<0.75:
            advice+=str(num)+'.'+'您上周碳水化合物摄入不足，若不及时调整，可能会造成营养不良，低血糖，易头晕心慌'+'\n'
            num+=1
        if x[2]>1.25:
            advice+=str(num)+'.'+'您上周碳水化合物摄入超标，若不及时调整，可能会变胖'+'\n'
            num+=1
        if x[3]<0.75:
            advice+=str(num)+'.'+'您上周维a摄入不足，若不及时调整，可能会导致皮肤干燥，夜盲症，发育迟缓，食欲减退等'+'\n'
            num+=1
        if x[3]>1.25:
            advice+=str(num)+'.'+'您上周维a摄入超标，若不及时调整，可能会维a慢性中毒，导致关节酸痛，脱发，头痛等'+'\n'
            num+=1
        if x[4]<0.75:
            advice+=str(num)+'.'+'您上周维b6摄入不足，若不及时调整，可能会导致口腔溃疡，脚气病，牙周炎，神经衰弱等'+'\n'
            num+=1
        if x[4]>1.25:
            advice+=str(num)+'.'+'您上周维b摄入超标，若不及时调整，可能会导致维b慢性中毒，头晕眼花，心律失常，发热呕吐'+'\n'
            num+=1
        if x[5]<0.75:
            advice+=str(num)+'.'+'您上周维c摄入不足，若不及时调整，可能会导致皮肤黏膜出血，骨骼病变，疲倦乏力'+'\n'
            num+=1
        if x[5]>1.25:
            advice+=str(num)+'.'+'您上周维c摄入超标，若不及时调整，可能会导致尿结石，产生骨骼疾病。'+'\n'
            num+=1
        if x[6]<0.75:
            advice+=str(num)+'.'+'您上周钙摄入不足，若不及时调整，可能会导致骨质疏松，抽筋，佝偻病，发育迟缓等'+'\n'
            num+=1
        if x[6]>1.25:
            advice+=str(num)+'.'+'您上周钙摄入超标，若不及时调整，可能会导致肠胃损伤，软组织钙化，泌尿系统结石'+'\n'
            num+=1
        if x[7]<0.75:
            advice+=str(num)+'.'+'您上周铁摄入不足，若不及时调整，可能会导致贫血，四肢无力，昏迷甚至休克'+'\n'
            num+=1
        if x[7]>1.25:
            advice+=str(num)+'.'+'您上周铁摄入超标，若不及时调整，可能会导致肺脾淋巴系统铁沉积，影响心脑血管，甚至食道癌大肠癌'+'\n'
            num+=1
        if x[8]<0.75:
            advice+=str(num)+'.'+'您上周锌摄入不足，若不及时调整，可能会发育不良，厌食挑食，免疫力低下'+'\n'
            num+=1
        if x[8]>1.25:
            advice+=str(num)+'.'+'您上周锌摄入超标，若不及时调整，可能会导致锌中毒，消化道糜烂出血，呼吸道炎症，神经功能障碍'+'\n'
            num+=1
        if x[9]<0.75:
            advice+=str(num)+'.'+'您上周膳食纤维摄入不足，若不及时调整，可能会引起痔疮，便秘，诱发结肠癌和心脑血管疾病'+'\n'
            num+=1
        if x[9]>1.25:
            advice+=str(num)+'.'+'您上周膳食纤维摄入超标，若不及时调整，可能会引起肠胃不适，影响无机盐的吸收'+'\n'
            num+=1
        if x[10]<0.75:
            advice+=str(num)+'.'+'您上周热量摄入不足，若不及时调整，可能会导致呆滞，记忆力减退，神志不清，浑身乏力'+'\n'
            num+=1
        if x[10]>1.25:
            advice+=str(num)+'.'+'您上周热量摄入超标，若不及时调整，可能会导致肥胖，进而诱发乳腺癌大肠癌'+'\n'
            num+=1
        return x,advice
    except:
        return [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0], ''
###  x是一个有11个浮点数的列表，例如x=[0.71,0.88,0.98,0.78,0.45,0.66,0.77,0.88,0.99,0.85]
#    比如x[0]=0.71,表示这周（总摄入蛋白质）比（推荐摄入）=71%
##   advice是字符串，表示给出的建议
# print(week_assess())



