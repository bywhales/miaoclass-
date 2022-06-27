# miaoclass_bot

## How to start

1. 切到 bot.py 所在文件夹 .
2. 进入终端使用命令'nb run'.

##help_txt
miaoclass --0.2.0
#更新时间：2022.06.28
## 命令插件 ##
src\plugins下的py文件


add\_class_main.py:
	添加课表

	def main(studentname: str, qqnumber):
		```
		根据姓名，将个人课表与QQ绑定
		```
		return 'QQ已绑定__的课表信息' or '导入成功' or '导入失败'	

	def main_by_number(studentname: str, qqnumber, times: int, student_number):
		```
		为了解决重名冲突，根据学号，将个人课表与QQ绑定
		两者区别：在实行浏览器操作时，执行多次下箭头按键，知道选择到学号指定学生
		```
		return 'QQ已绑定__的课表信息' or '导入成功' 


bound_deletion.py:
	绑定删除
	
bound_query.py:
	绑定查询

bound_update.py:
	绑定更新

chouqian.py:
	抽签，编写命令的基础模板

class_notice.py:
	课程通知功能，主要分为


1. 开启定时器
2. 解析数据库中的课表信息


good_night.py
	发送晚安信息

read\_60s_config.py
	每日60s读世界的配置文件

read\_60s_update.py
	每日60s读世界更新指令

read_60s.py
	每日60s读世界

	def remove_upprintable_chars(s):
		```
		去除URL中的不可见字符
        ```
		return URL


	async def read60s():
		```
		发送每日60s的函数
		```


	async def suijitu():
		```
		向每日60s读世界接口发起请求,并获得返回img的URL
		```

----------
src\plugins\miaoclass下的py文件


__init__.py
	闭包空函数

add_mysql.py
	向数据库中的添加操作

		def adduser(searchname, qqnumber):
			```
			向数据库中添加用户信息
			```
			return -1, -1 #用户已存在
			return student_number, times #添加成功


		def addclass(studentnumber, classname, weektime, weekjudge, place, student_qq_number):
			```
			向数据库中添加课表信息
			```  
			return None #无return

get_data.py
	根据HTML解析出课表数据

		def makeclassstr(classnameadd):
			```
			处理课名数据，用于分离单、多节课
			```
        	return classnameaddmaker #返回课名字符串


		def makeweektimestr(weektimeadd):
			```
			处理上课周数
			```
       		return weektimeaddmaker



		def makeweekjudgestr(weekjudgeadd):
			```
			处理单双周判断
			```
       		return weekjudgeadd #单节课的单双周判断
			return weekjudgeaddmaker #多节课的判断


		def makeplacestr(placeadd):
			```
			处理上课地点判断
			```
			return placeadd#单节课的上课地点判断
       		return placeaddmaker #多节课的判断


		def getdata(soup):
			```
			处理上课地点判断
			```
			return classname, weektime, weekjudge, place

scan_db.py
	扫描数据库操作

	def scandb(day, time):
		    return a #扫描指定课的结果


	def search_user_name(qqnumber):
		```
		根据QQ账号，在数据库中检索绑定用户姓名、学号
		```
			return studentnumber, name, qqnumber #正常返回
       		return 0 #QQ没有绑定信息

	def deletion_user_name(qqnumber):
		```
		根据QQ账号，在数据库中删除所绑定用户的信息
		```
			return 1 #删除成功
       		return 0 #QQ没有绑定信息


	def get_all_qq():
		```
		获取数据库中所有QQ账号
		```
			return all_qq_number #返回所有用户QQ列表

studentdata.py
	学生基本信息数据存储和查询文件

		def searchstudent(studentname):
		```
		根据姓名，检索学生学号
		```
			return bj[name:name+numlength+16]


		def judgeifduplication(studentname):
		```
		根据姓名，判断学生姓名是否存在重复
		```
			return nametimes.__len__() #返回重复次数
       		return 0 #返回无重复


		def judgeifduplicationtimes(studentname, student_number):

		```
		根据姓名、学号，判断需要按下箭头按键的次数
		```
			return nametimes, numbertimes #返回次数
			return 0 #返回错误


		def searchstudentbynumber(studentnumber):
		
		```
		通过学号检索学生信息
		```
			return name_data, numbertimes #???暂时没看明白，初步判断为返回姓名重复次数的


## Documentation


See [Docs](https://v2.nonebot.dev/)
