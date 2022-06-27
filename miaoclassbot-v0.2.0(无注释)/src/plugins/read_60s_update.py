from nonebot.adapters.onebot.v11 import Message, GroupMessageEvent
from nonebot import on_command


import requests
import json
weather = on_command("更新", priority=5)


@weather.handle()
async def receive(event: GroupMessageEvent):
    if(event.group_id == 738448935 or event.group_id == 413568705):
        msg = suijitu()
        await weather.send(message=Message(msg))


def remove_upprintable_chars(s):
    return ''.join(x for x in s if x.isprintable())  # 去除imageUrl可能存在的不可见字符


def suijitu():
    try:
        url = "https://api.iyk0.com/60s"
        resp = requests.get(url)
        resp = resp.text
        resp = remove_upprintable_chars(resp)
        retdata = json.loads(resp)
        lst = retdata['imageUrl']
        pic_ti = f"今日60S读世界已送达\n\n出错请发送“更新”\n [CQ:image,file={lst}]"
        return pic_ti
    except:
        url = "https://api.2xb.cn/zaob"  # 备用网址
        resp = requests.get(url)
        resp = resp.text
        resp = remove_upprintable_chars(resp)
        retdata = json.loads(resp)
        lst = retdata['imageUrl']
        pic_ti1 = f"今日60S读世界已送达\n\n出错请发送“更新”\n [CQ:image,file={lst}]"
        return pic_ti1
