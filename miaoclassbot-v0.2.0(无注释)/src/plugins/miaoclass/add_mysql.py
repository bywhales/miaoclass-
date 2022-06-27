# 导入pymysql模块
import pymysql
import nonebot

from . import studentdata

# 读取配置文件，获取数据库信息
host_data = nonebot.get_driver().config.host_data
port_data = nonebot.get_driver().config.port_data
root_name = nonebot.get_driver().config.root_name
root_password = nonebot.get_driver().config.root_password
db_name = nonebot.get_driver().config.db_name


def adduser(searchname, qqnumber):
    student_name_number = studentdata.searchstudent(searchname).split(',')
    studentnumber = int(float(student_name_number[1].strip("xh:'")))
    studentname = student_name_number[0].strip("'")
    studentid = studentnumber
    student = [studentnumber, studentname, qqnumber, studentid]
    connection = pymysql.connect(host=host_data, port=port_data, user=root_name, password=root_password, db=db_name,
                                 charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    searchsql = 'SELECT * FROM `studentname` WHERE `student_qq_number`=%r;' % student[2]
    a = cursor.execute(searchsql)
    connection.commit()
    if(a):
        return 0
    else:
        sql = "INSERT INTO `studentname` (`studentnumber`,`name`,`student_qq_number`,`studentID`) VALUES ({number},'{name}',{qqnumber},{id})".format(
            number=student[0], name=student[1], qqnumber=student[2], id=student[3]).encode('utf8')
        cursor.execute(sql)
        connection.commit()
        return studentnumber


def adduser_bynumber(searchname, qqnumber, student_number):
    student_name, times = studentdata.searchstudentbynumber(
        student_number)
    studentid = student_number
    student = [student_number, student_name, qqnumber, studentid]
    connection = pymysql.connect(host=host_data, port=port_data, user=root_name, password=root_password, db=db_name,
                                 charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    searchsql = 'SELECT * FROM `studentname` WHERE `student_qq_number`=%r;' % student[2]
    a = cursor.execute(searchsql)
    connection.commit()
    if(a):
        return -1, -1
    else:
        sql = "INSERT INTO `studentname` (`studentnumber`,`name`,`student_qq_number`,`studentID`) VALUES ({number},'{name}',{qqnumber},{id})".format(
            number=student[0], name=student[1], qqnumber=student[2], id=student[3]).encode('utf8')
        cursor.execute(sql)
        connection.commit()
        return student_number, times


def addclass(studentnumber, classname, weektime, weekjudge, place, student_qq_number):

    connection = pymysql.connect(host=host_data, port=port_data, user=root_name, password=root_password, db=db_name,
                                 charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    studentID = studentnumber

    Mon = []
    Tue = []
    Wed = []
    Thu = []
    Fri = []
    Sat = []
    Sun = []
    for i in range(5):
        i = int(i)
        Mon.append(classname[1+i*7] + '__' +
                   weektime[1+i*7]+'__'+weekjudge[1+i*7]+'__'+str(place[1+i*7]))
        Tue.append(classname[2+i*7] + '__' +
                   weektime[2+i*7]+'__'+weekjudge[2+i*7]+'__'+str(place[2+i*7]))
        Wed.append(classname[3+i*7] + '__' +
                   weektime[3+i*7]+'__'+weekjudge[3+i*7]+'__'+str(place[3+i*7]))
        Thu.append(classname[4+i*7] + '__' +
                   weektime[4+i*7]+'__'+weekjudge[4+i*7]+'__'+str(place[4+i*7]))
        Fri.append(classname[5+i*7] + '__' +
                   weektime[5+i*7]+'__'+weekjudge[5+i*7]+'__'+str(place[5+i*7]))
        Sat.append(classname[6+i*7] + '__' +
                   weektime[6+i*7]+'__'+weekjudge[6+i*7]+'__'+str(place[6+i*7]))
        Sun.append(classname[0+i*7] + '__' +
                   weektime[0+i*7]+'__'+weekjudge[0+i*7]+'__'+str(place[0+i*7]))
    for i in range(5):
        t = i*2
        n = t+1
        m = t+2
        sql = "INSERT INTO `class{n}{m}`VALUES ({studentID},'{student_qq_number}','{Mon12}','{Tue12}','{Wed12}','{Thu12}','{Fri12}','{Sat12}','{Sun12}')"\
            .format(n=n, m=m,
                    studentID=studentID, student_qq_number=student_qq_number, Mon12=Mon[i], Tue12=Tue[i], Wed12=Wed[i], Thu12=Thu[i], Fri12=Fri[i], Sat12=Sat[i], Sun12=Sun[i]).encode('utf8')

        cursor.execute(sql)
        connection.commit()
