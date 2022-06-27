# 导入nonebot.require模块
from nonebot import require
import nonebot


from .miaoclass import weather
from .miaoclass import scan_db

import datetime

scheduler = require('nonebot_plugin_apscheduler').scheduler


@scheduler.scheduled_job('cron', hour='23', minute='10')
async def run_every_hour():
    bot = nonebot.get_bot()
    message = weather.main()
    if(message):
        message = '晚安[CQ:face,id=75]\n'+message
        all_qq_number = scan_db.get_all_qq()
        for item in all_qq_number:
            await bot.send_private_msg(user_id=item, message=message)
