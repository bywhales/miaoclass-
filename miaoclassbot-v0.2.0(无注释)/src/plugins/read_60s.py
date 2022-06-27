from nonebot.adapters.onebot.v11 import Message
from nonebot import require


from .read_60s_config import Config
import requests
import nonebot
import json
global_config = nonebot.get_driver().config
nonebot.logger.info("global_config:{}".format(global_config))
plugin_config = Config(**global_config.dict())
nonebot.logger.info("plugin_config:{}".format(plugin_config))
scheduler = require("nonebot_plugin_apscheduler").scheduler


def remove_upprintable_chars(s):
    return ''.join(x for x in s if x.isprintable())


async def read60s():
    msg = await suijitu()
    for qq in plugin_config.read_qq_friends:
        await nonebot.get_bot().send_private_msg(user_id=qq, message=Message(msg))

    for qq_group in plugin_config.read_qq_groups:
        await nonebot.get_bot().send_group_msg(group_id=qq_group, message=Message(msg))


async def suijitu():
    try:
        url = "https://api.iyk0.com/60s"
        resp = requests.get(url)
        resp = resp.text
        resp = remove_upprintable_chars(resp)
        retdata = json.loads(resp)
        lst = retdata['imageUrl']
        pic_ti = f"今日60S读世界已送达\n\n出错请发送“更新”\n[CQ:image,file={lst}]"
        return pic_ti
    except:
        url = "https://api.2xb.cn/zaob"  # 备用网址
        resp = requests.get(url)
        resp = resp.text
        resp = remove_upprintable_chars(resp)
        retdata = json.loads(resp)
        lst = retdata['imageUrl']
        pic_ti1 = f"今日60S读世界已送达\n\n出错请发送“更新”\[CQ:image,file={lst}]"
        return pic_ti1

for index, time in enumerate(plugin_config.read_inform_time):
    nonebot.logger.info("id:{},time:{}".format(index, time))
    scheduler.add_job(read60s, "cron", hour=time.hour,
                      minute=time.minute, id=str(index))
