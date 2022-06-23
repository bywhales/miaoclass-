from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText

weather = on_command("抽签", rule=to_me(),  priority=5)


@weather.handle()
async def receive(matcher: Matcher, args: Message = CommandArg()):
    await weather.send('毋庸置疑的上上签，祝今日好运！')
