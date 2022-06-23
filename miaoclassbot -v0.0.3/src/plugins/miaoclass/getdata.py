# coding=utf-8
from bs4 import BeautifulSoup
import sys
import io
import re

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')

classname = []  # 课程名
teachername = []  # 老师名
weektime = []  # 上课周数
weekjudge = []  # 判断单双周
place = []  # 上课地点
rematch = r'<font.*font>'  # 匹配总数据 的re式
reclassname = r'">.*?</font>'  # 提取每项数据 的re式
remanyclassname = r'[)]">.*?</font>'
retechername = r'老师">.*?font>'
reweektime = r'周次">.*?</font>'
reweekjudge = r'单双周">.*?</font>'
replace = r'上课地点教室">.*?</font>'


def makeclassstr(classnameadd):
    len = classnameadd.__len__()
    i = 1
    classnameaddmaker = ''
    if(len == 1):
        classnameadd = str(classnameadd).strip("['\">").strip("</font>']")
        return classnameadd
    else:
        classnameadd = re.findall(reclassname, str(classnameadd))
        classnameaddmaker = str(classnameadd[0]).strip('">').strip(
            "</font>']")
        while i < len:
            classnameaddmaker = classnameaddmaker+'>>' + \
                str(re.findall(remanyclassname, str(classnameadd[i]))).strip(
                    "[')\">").strip("</font>']")
            i = i+1
        return classnameaddmaker


def makeweektimestr(weektimeadd):
    len = weektimeadd.__len__()
    i = 0
    weektimeaddmaker = ''
    if(len == 1):
        weektimeadd = str(weektimeadd).strip('[\'周次">').strip("</font>']")
        return weektimeadd
    else:
        while i < len:

            weektimeaddmaker = weektimeaddmaker+'>>'+str(weektimeadd[i]).strip(
                '\'周次">').strip('</font>\'')
            i = i+1
        return weektimeaddmaker


def makeweekjudgestr(weekjudgeadd):
    len = weekjudgeadd.__len__()
    weekjudgeaddmaker = ''
    i = 0
    if(len == 1):
        weekjudgeadd = str(weekjudgeadd)[7:-1].strip("</font>']")
        return weekjudgeadd
    else:
        while i < len:

            weekjudgeaddmaker = weekjudgeaddmaker+'>>'+str(weekjudgeadd[i])[
                5:-1].strip("</font>")
            i = i+1
        return weekjudgeaddmaker


def makeplacestr(placeadd):
    len = placeadd.__len__()
    placeaddmaker = ''
    i = 0
    if(len == 1):
        placeadd = str(placeadd)[10:-1].strip("</font>']")
        return placeadd
    else:
        while i < len:
            placeaddmaker = placeaddmaker+'>>'+str(placeadd[i])[
                7:-1].strip("</font>")
            i = i+1
        return placeaddmaker


def getdata(soup):
    tr = soup.findAll('tr')
    tr.pop(0)
    tr.pop()
    classname = []
    weektime = []
    weekjudge = []
    place = []
    for j in range(6):
        for i in range(7):
            td = str(tr[j]).split('<td')
            td.pop(0)
            td.pop(0)
            message = re.findall(rematch, td[i])

            if(message):
                # 各项数据提取和清洗
                classnameadd = re.findall(reclassname, message[0])
                classnameadd = makeclassstr(classnameadd)
                # teachernameadd = str(re.findall(retechername, message[1]))
                # teachernameadd = maketecherstr(teachernameadd)
                weektimeadd = re.findall(reweektime, message[1])
                weektimeadd = makeweektimestr(weektimeadd)
                weekjudgeadd = re.findall(reweekjudge, message[1])
                weekjudgeadd = makeweekjudgestr(weekjudgeadd)
                placeadd = re.findall(replace, message[1])
                placeadd = makeplacestr(placeadd)
                # 体育课等类型课没有固定上课地点，另外处理
                classname.append(classnameadd)
                # teachername.append(teachernameadd)
                weektime.append(weektimeadd)
                weekjudge.append(weekjudgeadd)
                place.append(placeadd)
            else:
                classname.append('')  # 没有课时加空数据占格子
                # teachername.append('')
                weektime.append('')
                weekjudge.append('')
                place.append('')
    return classname, weektime, weekjudge, place
