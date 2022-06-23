import pymysql
import sys
import io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
host_data = '127.0.0.1'
port_data = 3306
user_data = ''
password_data = ''
db_data = ''


def scandb(day, time):
    # 连接database
    # 连接MySQL数据库
    connection = pymysql.connect(host=host_data, port=port_data, user=user_data, password=password_data, db=db_data,
                                 charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    # 通过cursor创建游标
    cursor = connection.cursor()
    # 创建sql 语句，并执行
    # deletesql = 'DELETE  FROM `studentname` WHERE 1=1;'
    # cursor.execute(deletesql)
    # connection.commit()
    weekday = ['', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    daystr = weekday[day]+str(time)
    classstr = 'class'+str(time)
    sql = "SELECT `studentname`.`qqnumber`, \
        `{class12}`.`studentID`, `{class12}`.`{daystr}` FROM `studentname`, \
            `{class12}`WHERE(`studentname`.`studentID`=`{class12}`.`studentID`)"\
                .format(class12=classstr, daystr=daystr)
    cursor.execute(sql)
    connection.commit()
    a = cursor.fetchall()
    return a


async def search_user_name(qqnumber):
    connection = pymysql.connect(host=host_data, port=port_data, user=user_data, password=password_data, db=db_data,
                                 charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    # 通过cursor创建游标
    cursor = connection.cursor()
    sql = "SELECT `studentnumber`,`name`,`qqnumber` FROM `studentname` WHERE `qqnumber`=%s; "\
        % qqnumber
    cursor.execute(sql)
    a = cursor.fetchall()
    connection.commit()
    if(a):
        studentnumber = a[0]['studentnumber']
        name = a[0]['name']
        qqnumber = a[0]['qqnumber']
        return studentnumber, name, qqnumber
    else:
        return 0


def deletion_user_name(qqnumber):
    result = search_user_name(qqnumber)
    if(result == 0):
        return 0
    else:
        connection = pymysql.connect(host=host_data, port=port_data, user=user_data, password=password_data, db=db_data,
                                     charset='utf8', cursorclass=pymysql.cursors.DictCursor)
        # 通过cursor创建游标
        cursor = connection.cursor()
        sql = "DELETE  FROM `studentname` WHERE `qqnumber`=%s;" % qqnumber
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
