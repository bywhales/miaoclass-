from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.adapters.onebot.v11 import PrivateMessageEvent
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

import time
from .miaoclass import getdata
from .miaoclass import studentdata
from .miaoclass import addmysqltest

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument('ignore-certificate-errors')
driver = webdriver.Chrome(options=options)
url = 'http://csujwc.its.csu.edu.cn/jiaowu/pkgl/llsykb/llsykb_find_xs0101.jsp?xnxq01id=2021-2022-2&init=1&isview=0'
driver.get(url)  # 使用浏览器打开url
weather = on_command(
    "add", aliases={'添加用户', '绑定用户', '绑定'}, rule=to_me(),  priority=1)


@weather.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数
    if plain_text:
        matcher.set_arg("cy", args)  # 如果用户发送了参数则直接赋值


@weather.got("cy", prompt="请输入姓名")
async def handle_name(event: PrivateMessageEvent, student_name: str = ArgPlainText("cy")):
    studentname = str(student_name)
    qqnumber = event.get_user_id()
    judgekey = studentdata.judgeifduplication(studentname)
    if judgekey == 1:
        addkey = main(studentname, qqnumber)
        await weather.finish(addkey)
    elif judgekey == 0:
        await weather.finish('%r信息不存在,请重新使用指令 add 添加用户' % studentname)
    else:
        await weather.send('姓名%r存在重复' % studentname)


@weather.got("number", prompt="请输入学号")
async def handle_number(event: PrivateMessageEvent, student_number: str = ArgPlainText("number")):
    student_number = str(student_number)
    qqnumber = event.get_user_id()
    studentname, times = studentdata.searchstudentbynumber(student_number)
    addkey = await main_by_number(studentname, qqnumber, times, student_number)
    await weather.finish(addkey)


def main(studentname: str, qqnumber):
    # ------------------------------------------------------------------------
    studentnumber = addmysqltest.adduser(studentname, qqnumber)
    # 查询添加学生信息后，返回学生学号或者错误0
    if(studentnumber == 0):
        return 'QQ已绑定%r的课表信息' % studentname
    # ------------------------------------------------------------------------

    element_input = driver.find_element(By.ID, "xs")  # 获得输入框DOM
    element_search = driver.find_element(
        By.CLASS_NAME, 'button')  # 获得提交按钮DOM
    element_input.clear()  # 输入框清零
    element_input.send_keys(studentname)  # 输入框写入 姓名
    time.sleep(0.05)
    element_input.send_keys(Keys.ENTER)  # 执行键盘的回车事件
    time.sleep(0.05)
    element_search.click()      # 执行按钮的点击事件
    time.sleep(2)
    iframe = driver.find_elements(By.TAG_NAME, 'iframe')[
        1]  # 捕捉数据所在iframe的DOM节点
    driver.switch_to.frame(iframe)  # 深入iframe框架解析

    soup = BeautifulSoup(driver.page_source, "html.parser")  # 熬汤

    classname, weektime, weekjudge, palce = getdata.getdata(
        soup)  # 解析汤，获取数据
    addmysqltest.addclass(studentnumber, classname,
                          weektime, weekjudge, palce, qqnumber)
    driver.switch_to.parent_frame()
    return '导入成功'


async def main_by_number(studentname: str, qqnumber, times: int, student_number):
    # ------------------------------------------------------------------------
    studentnumber, times = addmysqltest.adduser_bynumber(
        studentname, qqnumber, student_number)
    # 查询添加学生信息后，返回学生学号或者错误0
    if(times == 0):
        return 'QQ已绑定%r的课表信息' % studentname
    # ------------------------------------------------------------------------
    element_input = driver.find_element(By.ID, "xs")  # 获得输入框DOM
    element_search = driver.find_element(By.CLASS_NAME, 'button')  # 获得提交按钮DOM
    element_input.clear()  # 输入框清零
    element_input.send_keys(studentname)  # 输入框写入 姓名
    time.sleep(0.05)
    for i in range(times):
        element_input.send_keys(Keys.DOWN)
    time.sleep(0.05)
    element_input.send_keys(Keys.ENTER)  # 执行键盘的回车事件
    time.sleep(0.05)
    element_search.click()      # 执行按钮的点击事件
    time.sleep(2)
    iframe = driver.find_elements(By.TAG_NAME, 'iframe')[
        1]  # 捕捉数据所在iframe的DOM节点
    driver.switch_to.frame(iframe)  # 深入iframe框架解析

    soup = BeautifulSoup(driver.page_source, "html.parser")  # 熬汤

    classname, weektime, weekjudge, palce = getdata.getdata(
        soup)  # 解析汤，获取数据
    addmysqltest.addclass(studentnumber, classname,
                          weektime, weekjudge, palce, qqnumber)
    driver.switch_to.parent_frame()
    return '导入成功'
