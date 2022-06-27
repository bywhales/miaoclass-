from nonebot.adapters.onebot.v11 import PrivateMessageEvent
from nonebot.params import CommandArg, ArgPlainText
from selenium.webdriver.common.keys import Keys
from nonebot.adapters import Message
from nonebot.matcher import Matcher
from nonebot.rule import to_me
from nonebot import on_command

from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import time

from .miaoclass import studentdata
from .miaoclass import add_mysql
from .miaoclass import get_data
from .miaoclass import scan_db
options = webdriver.FirefoxOptions()
driver = webdriver.Firefox(options=options)
url = 'http://csujwc.its.csu.edu.cn/jiaowu/pkgl/llsykb/llsykb_find_xs0101.jsp?xnxq01id=2022-2023-1&init=1&isview=0'
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
    addkey = main_by_number(studentname, qqnumber, times, student_number)
    await weather.finish(addkey)


def main(studentname: str, qqnumber):
    try:
        studentnumber = add_mysql.adduser(studentname, qqnumber)
        result = scan_db.search_user_name(qqnumber)
        if(studentnumber == 0):
            return 'QQ已绑定%r的课表信息' % result[1]

        element_input = driver.find_element(By.ID, "xs")
        element_search = driver.find_element(
            By.CLASS_NAME, 'button')
        element_input.clear()
        element_input.send_keys(studentname)
        time.sleep(1)
        element_input.send_keys(Keys.ENTER)
        time.sleep(1)
        element_search.click()
        time.sleep(5)
        iframe = driver.find_elements(By.TAG_NAME, 'iframe')[1]
        driver.switch_to.frame(iframe)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        classname, weektime, weekjudge, palce = get_data.getdata(soup)
        add_mysql.addclass(studentnumber, classname,
                           weektime, weekjudge, palce, qqnumber)
        return '导入成功'
    except:
        return '导入失败'
    finally:
        driver.switch_to.parent_frame()


def main_by_number(studentname: str, qqnumber, times: int, student_number):
    try:
        studentnumber, times = add_mysql.adduser_bynumber(
            studentname, qqnumber, student_number)
        if(times == 0):
            return 'QQ已绑定%r的课表信息' % studentname
        element_input = driver.find_element(By.ID, "xs")
        element_search = driver.find_element(By.CLASS_NAME, 'button')
        element_input.clear()
        element_input.send_keys(studentname)
        time.sleep(0.5)
        for i in range(times):
            element_input.send_keys(Keys.DOWN)
            time.sleep(0.05)
        time.sleep(0.5)
        element_input.send_keys(Keys.ENTER)
        time.sleep(0.5)
        element_search.click()
        time.sleep(2)
        iframe = driver.find_elements(By.TAG_NAME, 'iframe')[1]
        driver.switch_to.frame(iframe)

        soup = BeautifulSoup(driver.page_source, "html.parser")  # 熬汤

        classname, weektime, weekjudge, palce = get_data.getdata(
            soup)
        add_mysql.addclass(studentnumber, classname,
                           weektime, weekjudge, palce, qqnumber)
        driver.switch_to.parent_frame()
        return '导入成功'
    except:
        return '导入失败'
    finally:
        driver.switch_to.parent_frame()
