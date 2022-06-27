from nonebot.rule import to_me
from nonebot import on_command

weather = on_command("抽签", rule=to_me(),  priority=5)


@weather.handle()
async def receive():
    await weather.send('毋庸置疑的上上签，祝今日好运！')
