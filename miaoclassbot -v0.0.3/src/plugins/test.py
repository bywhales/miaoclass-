from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText

weather = on_command("weather", rule=to_me(),  priority=5)


@weather.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    if plain_text:
        matcher.set_arg("cy", args)  # 如果用户发送了参数则直接赋值


@weather.got("cy", prompt="你想查询哪个城市的天气呢？")
async def handle_city(city_name: str = ArgPlainText("cy")):
    # if city_name not in ["北京", "上海"]:  # 如果参数不符合要求，则提示用户重新输入
    #     # 可以使用平台的 Message 类直接构造模板消息
    #     await weather.reject(cy.template("你想查询的城市 {cy} 暂不支持，请重新输入！"))

    city_weather = await get_weather(city_name)
    await weather.finish(city_weather)


# 在这里编写获取天气信息的函数
async def get_weather(city: str):
    city = '修改后的'+city
    return f"{city}的天气是..."
