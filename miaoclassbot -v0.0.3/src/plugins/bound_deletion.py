from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.adapters.onebot.v11 import PrivateMessageEvent

from .miaoclass import scandb
weather = on_command("绑定删除", aliases={'删除绑定', '信息删除', '删除信息'},
                     rule=to_me(),  priority=5)


@weather.handle()
async def receive(matcher: Matcher, event: PrivateMessageEvent, args: Message = CommandArg()):
    qqnumber = event.get_user_id()
    result = scandb.deletion_user_name(qqnumber)
    if(result == 0):
        await weather.send('无绑定信息')
    else:
        await weather.send('绑定信息已删除')
