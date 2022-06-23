# 导入pymysql模块
from unicodedata import name
from numpy import append, number
import pymysql
import sys
import io
from . import studentdata
host_data = '127.0.0.1'
port_data = 3306
user_data = ''
password_data = ''
db_data = ''


def adduser(searchname, qqnumber):
    student_name_number = studentdata.searchstudent(searchname).split(',')
    studentnumber = int(float(student_name_number[1].strip("xh:'")))
    studentname = student_name_number[0].strip("'")
    studentid = studentnumber
    student = [studentnumber, studentname, qqnumber, studentid]
    # 连接database
    # 连接MySQL数据库
    connection = pymysql.connect(host=host_data, port=port_data, user=user_data, password=password_data, db=db_data,
                                 charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    # 通过cursor创建游标
    cursor = connection.cursor()
    searchsql = 'SELECT * FROM `studentname` WHERE `qqnumber`=%r;' % student[2]
    a = cursor.execute(searchsql)
    connection.commit()
    if(a):
        return 0
    else:
        sql = "INSERT INTO `studentname` (`studentnumber`,`name`,`qqnumber`,`studentID`) VALUES ({number},'{name}',{qqnumber},{id})".format(
            number=student[0], name=student[1], qqnumber=student[2], id=student[3]).encode('utf8')
        cursor.execute(sql)
    # 提交SQL
        connection.commit()
        return studentnumber


def adduser_bynumber(searchname, qqnumber, student_number):
    student_name, times = studentdata.searchstudentbynumber(
        student_number)
    studentid = student_number
    student = [student_number, student_name, qqnumber, studentid]
    # 连接database
    # 连接MySQL数据库
    connection = pymysql.connect(host=host_data, port=port_data, user=user_data, password=password_data, db=db_data,
                                 charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    # 通过cursor创建游标
    cursor = connection.cursor()
    searchsql = 'SELECT * FROM `studentname` WHERE `qqnumber`=%r;' % student[2]
    a = cursor.execute(searchsql)
    connection.commit()
    if(a):
        return 0, 0
    else:
        sql = "INSERT INTO `studentname` (`studentnumber`,`name`,`qqnumber`,`studentID`) VALUES ({number},'{name}',{qqnumber},{id})".format(
            number=student[0], name=student[1], qqnumber=student[2], id=student[3]).encode('utf8')
        cursor.execute(sql)
    # 提交SQL
        connection.commit()
        return student_number, times


def addclass(studentnumber, classname, weektime, weekjudge, place, student_qq_number):  #

    connection = pymysql.connect(host=host_data, port=port_data, user=user_data, password=password_data, db=db_data,
                                 charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    # 通过cursor创建游标
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
        sql = "INSERT INTO `class{n}{m}`VALUES ({studentID},'{qq_number}','{Mon12}','{Tue12}','{Wed12}','{Thu12}','{Fri12}','{Sat12}','{Sun12}')"\
            .format(n=n, m=m,
                    studentID=studentID, qq_number=student_qq_number, Mon12=Mon[i], Tue12=Tue[i], Wed12=Wed[i], Thu12=Thu[i], Fri12=Fri[i], Sat12=Sat[i], Sun12=Sun[i]).encode('utf8')

        cursor.execute(sql)
        # 提交SQL
        connection.commit()
