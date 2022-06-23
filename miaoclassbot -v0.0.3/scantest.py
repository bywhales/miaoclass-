from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.adapters.onebot.v11 import PrivateMessageEvent
import pymysql
weather = on_command("课表", rule=to_me(),  priority=5)


@weather.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数
    if plain_text:
        matcher.set_arg("key", args)  # 如果用户发送了参数则直接赋值


@weather.got("key", prompt="你想查询哪个时间段的课表呢？")
async def handle_key(event: PrivateMessageEvent, key: str = ArgPlainText("key")):
    key = key.split('，')
    keyword = await scandb('a', key[0], key[1])
    await weather.finish(keyword)


# 在这里编写函数
async def scandb(a: str, day: int, time: int):
    # 连接database
    # 连接MySQL数据库
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='a417102322', db='test01',
                                 charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    # 通过cursor创建游标

    cursor = connection.cursor()
    # 创建sql 语句，并执行
    # deletesql = 'DELETE  FROM `studentname` WHERE 1=1;'
    # cursor.execute(deletesql)
    # connection.commit()
    weekday = ['', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

    daystr = weekday[day]+str(time)
    classstr = 'class'+str(time)
    sql = "SELECT `studentname`.`qqnumber`, \
        `{class12}`.`studentID`, `{class12}`.`{daystr}` FROM `studentname`, \
            `{class12}`WHERE(`studentname`.`studentID`=`{class12}`.`studentID`)"\
                .format(class12=classstr, daystr=daystr)
    # print(sql)
    a = ''
    cursor.execute(sql)
    a = str(cursor.fetchall())
    connection.commit()
    return f"{a}"
