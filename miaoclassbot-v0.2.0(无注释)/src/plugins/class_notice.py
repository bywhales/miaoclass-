# 导入nonebot.require模块
from nonebot import require
import nonebot

import datetime


from .miaoclass import scan_db


scheduler = require('nonebot_plugin_apscheduler').scheduler


@scheduler.scheduled_job('cron', hour='7', minute='35')
@scheduler.scheduled_job('cron', hour='9', minute='35')
@scheduler.scheduled_job('cron', hour='13', minute='35')
@scheduler.scheduled_job('cron', hour='15', minute='35')
@scheduler.scheduled_job('cron', hour='18', minute='35')
async def run_every_hour():
    datestart = datetime.datetime(2022, 2, 20)
    datenow = str(datetime.datetime.now())[0:10].split('-')
    datenow = datetime.datetime(
        int(datenow[0]), int(datenow[1]), int(datenow[2]))
    nowweeknumber_time = (int((datenow-datestart).days/7)+1)
    bot = nonebot.get_bot()
    week_time = datetime.datetime.now().strftime('%a')
    classhour_time = int(datetime.datetime.now().strftime('%H'))
    classmin_time = int(datetime.datetime.now().strftime('%M'))
    weekday = {'': 0, 'Mon': 1, 'Tue': 2, 'Wed': 3,
               'Thu': 4, 'Fri': 5, 'Sat': 6, 'Sun': 7}
    class_time = 0
    if classhour_time == 7 and classmin_time == 55:
        class_time = 12
    elif classhour_time == 9 and classmin_time == 35:
        class_time = 34
    elif classhour_time == 13 and classmin_time == 35:
        class_time = 56
    elif classhour_time == 15 and classmin_time == 35:
        class_time = 78
    elif classhour_time == 18 and classmin_time == 35:
        class_time = 910

    if class_time == 0:
        return 0
    qquser = []
    classname = []
    classplace = []
    dbresult = scan_db.scandb(weekday[week_time], class_time)

    for item in dbresult:
        classcontent = str(item[week_time+str(class_time)]).split('__')
        nowclassname = classcontent[0].split('>>')
        ifweeksend = classcontent[1].split('>>')
        weeklisttime = []
        if(ifweeksend.__len__() > 1 or ifweeksend[0] == ''):
            ifweeksend.pop(0)
        for ifweeksend_solojudge in range(ifweeksend.__len__()):
            ifweeksendadd = ifweeksend[ifweeksend_solojudge].split(',')
            allweek = []
            for ifweeksend_manyjudge in range(ifweeksendadd.__len__()):
                ifweeksendadd[ifweeksend_manyjudge] = ifweeksendadd[ifweeksend_manyjudge].split(
                    '-')
                if(ifweeksendadd[ifweeksend_manyjudge].__len__() > 1):

                    weeknum = int(ifweeksendadd[ifweeksend_manyjudge][1].strip('>>')) - \
                        int(ifweeksendadd[ifweeksend_manyjudge][0].strip('>>'))
                    weekstart = int(ifweeksendadd[ifweeksend_manyjudge][0])
                    weekend = weekstart+weeknum
                    allweek = allweek + list(range(weekstart, weekend+1))
                else:
                    weekone = int(ifweeksendadd[ifweeksend_manyjudge][0])
                    allweek = allweek + [weekone]
            if(nowweeknumber_time in allweek):
                weeklisttime.append(1)
                continue
            else:
                weeklisttime.append(0)
        ifsingledoubleweek = classcontent[2].split('>>')
        if(ifsingledoubleweek.__len__() > 1):
            ifsingledoubleweek.pop(0)
        singledoubuleweek = []
        for ifsingledoubleweek_solojudge in range(ifsingledoubleweek.__len__()):
            if(ifsingledoubleweek[ifsingledoubleweek_solojudge] == '单周' and nowweeknumber_time % 2 == 1):
                singledoubuleweek.append('1')
            elif(ifsingledoubleweek[ifsingledoubleweek_solojudge] == '双周' and nowweeknumber_time % 2 == 0):
                singledoubuleweek.append('1')
            elif(ifsingledoubleweek[ifsingledoubleweek_solojudge] == '周'):
                singledoubuleweek.append('1')
            else:
                singledoubuleweek.append('0')
        nowclassplace = classcontent[3].split('>>')
        if(nowclassplace.__len__() > 1):
            nowclassplace.pop(0)
        for classsend in range(nowclassname.__len__()):
            if(not classcontent[0] == '' and weeklisttime[classsend] and singledoubuleweek[classsend]):
                qquser.append(item['qqnumber'])
                classname.append(nowclassname[classsend])
                classplace.append(nowclassplace[classsend])
    for id in range(qquser.__len__()):
        if(not classplace[id] == ''):
            nextclassname = '回声测试\n'+'下一节课 \n' + \
                classname[id]+'\n上课地点：'+classplace[id]
        else:
            nextclassname = '回声测试\n'+'下一节课 \n' +\
                classname[id]
        await bot.send_private_msg(user_id=qquser[id], message=nextclassname)
