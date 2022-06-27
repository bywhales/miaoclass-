import pymysql
import nonebot

# 读取配置文件，获取数据库信息
host_data = nonebot.get_driver().config.host_data
port_data = nonebot.get_driver().config.port_data
root_name = nonebot.get_driver().config.root_name
root_password = nonebot.get_driver().config.root_password
db_name = nonebot.get_driver().config.db_name


def scandb(day, time):
    connection = pymysql.connect(host=host_data, port=port_data, user=root_name, password=root_password, db=db_name,
                                 charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    weekday = ['', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    daystr = weekday[day]+str(time)
    classstr = 'class'+str(time)
    sql = "SELECT `studentname`.`student_qq_number`, \
        `{class12}`.`studentID`, `{class12}`.`{daystr}` FROM `studentname`, \
            `{class12}`WHERE(`studentname`.`studentID`=`{class12}`.`studentID`)"\
                .format(class12=classstr, daystr=daystr)
    cursor.execute(sql)
    connection.commit()
    a = cursor.fetchall()
    return a


def search_user_name(qqnumber):
    connection = pymysql.connect(host=host_data, port=port_data, user=root_name, password=root_password, db=db_name,
                                 charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    sql = "SELECT `studentnumber`,`name`,`student_qq_number` FROM `studentname` WHERE `student_qq_number`=%s; "\
        % qqnumber
    cursor.execute(sql)
    a = cursor.fetchall()
    connection.commit()
    if(a):
        studentnumber = a[0]['studentnumber']
        name = a[0]['name']
        qqnumber = a[0]['student_qq_number']
        return studentnumber, name, qqnumber
    else:
        return 0


def deletion_user_name(qqnumber):
    result = search_user_name(qqnumber)
    if(result == 0):
        return 0
    else:
        connection = pymysql.connect(host=host_data, port=port_data, user=root_name, password=root_password, db=db_name,
                                     charset='utf8', cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor()
        sql = "DELETE  FROM `studentname` WHERE `student_qq_number`=%s;" % qqnumber
        cursor.execute(sql)
        connection.commit()
        for i in range(5):
            x = (i+1)*2-1
            y = (i+1)*2
            m = str(x)+str(y)
            sql = "DELETE  FROM `class%s` WHERE `student_qq_number`=%s;" % (
                m, qqnumber)
            cursor.execute(sql)
            connection.commit()
        return 1


def get_all_qq():
    connection = pymysql.connect(host=host_data, port=port_data, user=root_name, password=root_password, db=db_name,
                                 charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    sql = "SELECT `student_qq_number` FROM `studentname`;"
    cursor.execute(sql)
    a = cursor.fetchall()
    connection.commit()
    all_qq_number = []
    for item in a:
        all_qq_number.append(item['student_qq_number'])
    return all_qq_number
