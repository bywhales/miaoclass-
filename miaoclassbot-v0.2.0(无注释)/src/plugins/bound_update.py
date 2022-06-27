from nonebot.adapters.onebot.v11 import PrivateMessageEvent
from nonebot.rule import to_me
from nonebot import on_command

from . import add_class_main

from .miaoclass import studentdata
from .miaoclass import scan_db

weather = on_command("绑定更新", aliases={'更新绑定', '信息更新', '更新信息'},
                     rule=to_me(),  priority=4)


@weather.handle()
async def receive(event: PrivateMessageEvent):
    qqnumber = event.get_user_id()
    result = scan_db.search_user_name(qqnumber)
    name, times = studentdata.searchstudentbynumber(result[0])
    scan_db.deletion_user_name(qqnumber)
    result = add_class_main.main_by_number(
        result[1], result[2], times, result[0])
    if(result == '导入成功'):
        await weather.send('绑定更新成功')
    else:
        await weather.send('绑定更新失败')
