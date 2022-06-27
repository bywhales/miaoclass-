from nonebot.adapters.onebot.v11 import PrivateMessageEvent
from nonebot.rule import to_me
from nonebot import on_command

from .miaoclass import scan_db
weather = on_command("绑定删除", aliases={'删除绑定', '信息删除', '删除信息'},
                     rule=to_me(),  priority=5)


@weather.handle()
async def receive(event: PrivateMessageEvent):
    qqnumber = event.get_user_id()
    result = scan_db.deletion_user_name(qqnumber)
    if(not result):
        await weather.send('无绑定信息')
    else:
        await weather.send('绑定信息已删除')
