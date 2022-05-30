# -*- coding: utf-8 -*-
import requests
import time
import csv
import pandas as pd
import re
import s
from selenium import webdriver
from lxml import html
from selenium.webdriver.chrome.options import Options
 
options = Options()
options.headless = True
driver = webdriver.Chrome(executable_path="./chromedriver",chrome_options=options)

def get_url():
    # 目标url
    url = "https://mp.weixin.qq.com/cgi-bin/appmsg"
    
    # 使用Cookie，跳过登陆操作
    # Cooike需定期更换
    headers = {
      "Cookie": "pgv_pvid=9045712636; RK=9kpkGMeqHX; ptcz=dfa5074844c039eefb83d294a1b5a4045f68a10320b3e6ba476175876840b0e9; o_cookie=1091485663; pac_uid=1_1091485663; iip=0; ua_id=SLKZWnCJagf9GSjmAAAAALYGf5akrubbjZSJ7IUzDB4=; wxuin=52550558717279; wxopenid=; psrf_qqunionid=F32AD487847FA8659912A13239891D1A; euin=oKnqoKvF7KCsoz**; psrf_qqaccess_token=E18A23D7F76EB78A28A372EB4D638590; wxunionid=; wxrefresh_token=; psrf_qqrefresh_token=E1746AF4CFCE286ABFE2E5ABFD519652; psrf_access_token_expiresAt=1660824903; uin=1091485663; psrf_qqopenid=CD1C5D00F9D19D9504F7897831031608; tmeLoginType=2; fqm_pvqid=b6b65482-d850-4004-9fe5-020219dafa02; uuid=7af4441bf4bbd5f01710ed45ee11c493; rand_info=CAESIKsj4q0wiWc13JP1G0jloEyxcF1NRXp/qvKsNKpYrgA5; slave_bizuin=3897806706; data_bizuin=3897806706; bizuin=3897806706; data_ticket=cnLP0gHqTuA0WyaVGX7E1Ziozk7dQQgQT3kMy5PHdntjRL1I3LEE5WAxmdTvx4fQ; slave_sid=bjRYZjJ1c2pmb2FiVEp4dXcyWWVuZlVSNjd6OE9Gb3F3R2pHQ1A3MTJKb0RLTk8ybW1oSUYxWlRCNmJVYmRUNFFGY2hXMFJLREFUdFpNb2lXNXRBcHVOdTNZYjN2Vm5vOUp2VjdDQzlsMGxweEU1NWNRYU8xYngyN0pkaEFXaDFxdVRqSmhUaUdkdmZhNE15; slave_user=gh_333e5f03b0b3; xid=b61bba79da46c00b64bdaa4bc8a20a84; mm_lang=zh_CN; rewardsn=; wxtokenkey=777; wwapp.vid=; wwapp.cst=; wwapp.deviceid=",
      "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36",
    }
    
    data = {
        "token": "434108921",#token需要定期更换
        "lang": "zh_CN",
        "f": "json",
        "ajax": "1",
        "action": "list_ex",
        "begin": "0",
        "count": "5",
        "query": "",
        "fakeid": "MzU4NzI3ODUyNA==",#每个公众号有一个独一无二的fakeid
        "type": "9",
    }
    
    for i in range(20):#搜寻最新的D楼学生食谱
        data["begin"] = i*5
        time.sleep(3)
        # 使用get方法进行提交
        content_json = requests.get(url, headers=headers, params=data).json()
        # 返回了一个json，里面是每一页的数据
        for item in content_json["app_msg_list"]:    
        # 提取每页文章的标题及对应的url
            if(item["title"][0]!='D'):
                continue
            return item["link"]

def process_Url(url):
    driver.get(url)
    # 获取页面源代码
    html_source = driver.page_source
    # 重点
    Html = html.fromstring(html_source)
    # 获取标签下所有文本
    items = Html.xpath("//div[@id='js_content']//text()")
    # 正则 匹配以下内容 \s+ 首空格 \s+$ 尾空格 \n 换行
    pattern = re.compile("^\s+|\s+$|\n")
    estract_Dishes(pattern,items)

def estract_Dishes(pattern, items):
    today_menu_list=list()
    Dishes = set()
    flag=0;
    
    for item in items:
        # 将匹配到的内容用空替换，即去除匹配的内容，只留下文本
        line = re.sub(pattern, "", item)
        if len(line) > 0:
            flag+=1
            
            if(len(line) > 4):
                tmp = line[0] + line [1] + line[2] + line[3]
                if(tmp == "学生食堂"):
                    continue 
                    
            line = line.replace("   ","、")
            if(flag >= 13 and line[0] !="早" and line[0] !="午" and line[0] !="晚" and line[0] !="扫"
                and (not line[0].isdigit()) and (line[0]<'a' or line[0] >'z') and (line[0]<'A' or line[0]>'Z')):
                # clause_text += line + "\n"
                line = re.split('、|，',line)
                for ele in line:
                    ele = ele.replace("免费","")
                    l = len(ele)
                    #去除掉结尾的xx元
                    if(l > 3):
                        if(ele[l-1] == "元" and ele[l-2].isdigit()):
                            if(ele[l-3].isdigit()):
                                ele = ele[:l-3]
                            else:
                                ele = ele[:l-2]
                    l = len(ele)
                    #去除掉结尾的XX斤
                    if(l > 3):
                        if(ele[l-1] == "斤" and ele[l-2].isdigit()):
                            if(ele[l-3].isdigit()):
                                ele = ele[:l-3]
                            else:
                                ele = ele[:l-2]
                    Dishes.add(ele)
                    
    for dish in Dishes:
        query=list()
        query.append(dish)
        res = s.get_nutrition(query) # 查询该菜品在数据库中是否存在，不存在则不添加
        if(len(res) == 0):
            continue
        # print(dish)
        today_menu_list.append(dish)
    
    s.add2_todaymenu(today_menu_list) # 将菜品添加到当日菜品库中
        
                
if __name__ == '__main__':#直接调用main运行即可
    process_Url(get_url())    
    