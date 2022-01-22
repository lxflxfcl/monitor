
import sqlite3
import datetime


#创建数据库连接池
def conn_db():
    con = sqlite3.connect("cve_db.db")
    cursor = con.cursor()
    return cursor,con

#判断数据库是否为空
def is_database_empty():
    cursor,con = conn_db()
    sql = "select count(*) from cve_info"
    try:
        cursor.execute(sql)
        info = cursor.fetchone()
        if info[0] == 0:
            print("[*]当前数据库为空，数据库马上初始化.....")
            return True

        else:
            return False
    except Exception as e:
        print(e)

#数据库插入操作
def insertTo(values):
    sql = 'insert into cve_info values('+values+ ')'
    cursor,con = conn_db()
    try:
        cursor.execute(sql)
        cursor.close()
        con.commit()
        con.close()
    except Exception as e:
        print(e)

#数据库插入微软数据操作
def insertToMS(values_ms):
    sql_ms = 'insert into cve_info_ms values(' + values_ms + ')'
    #print(sql_ms)
    cursor,con = conn_db()
    try:
        cursor.execute(sql_ms)
        cursor.close()
        con.commit()
        con.close()
    except Exception as e:
        print(e)

#最新漏洞消息、程序报错消息写到日志中，便于后期审查
def write_log(log_time,msg):
    log_file_name ='./log/' + str(datetime.datetime.now().date()) + '.log'
    with open(log_file_name,'a') as f:
        f.write(log_time + " " + msg + "\n")
    f.close()

#判断某条漏洞信息是否在数据库中存在
def is_not_exist(one_info):
    log_update_time = str(datetime.datetime.now().ctime())
    cursor,con = conn_db()
    sql = "select * from cve_info where cnnvd_num=?"
    try:
        cursor.execute(sql,(str(one_info[2]),))
        info = cursor.fetchone()
        #print(info)
        if info == None:
            insert_msg = "[*]有最新CNNVD编号漏洞:" + one_info[2]
            print(insert_msg)
            write_log(log_update_time,insert_msg)
            return True
        print("[!]无最新CNNVD编号")
        return False
    except Exception as e:
        error_msg = "[x]ERROR: " + str(e)
        print(error_msg)
        write_log(log_update_time,error_msg)
        return False
    finally:
        cursor.close()
        con.close()

#判断某条微软漏洞信息是否在数据库中存在
def is_not_exist_ms(one_info):
    log_update_time = str(datetime.datetime.now().ctime())
    cursor,con = conn_db()
    sql = "select * from cve_info_ms where cve_num=?"
    try:
        cursor.execute(sql,(str(one_info[1]),))
        info = cursor.fetchone()
        #print(info)
        if info == None:
            insert_msg = "[*]有最新微软CVE编号漏洞:" + one_info[1]
            print(insert_msg)
            write_log(log_update_time,insert_msg)
            return True
        print("[!]无最新微软CVE编号")
        return False
    except Exception as e:
        error_msg = "[x]ERROR: " + str(e)
        print(error_msg)
        write_log(log_update_time,error_msg)
        return False
    finally:
        cursor.close()
        con.close()
#判断数据库是否为空


#查询漏洞信息危害级别
def danger_level_nums():
    cursor,con = conn_db()
    #sql = "select danger_level, count(*) from cve_info  where  danger_level='中危'"
    if datetime.datetime.now().weekday() + 1 == 5:

        sql = "SELECT  danger_level,count(*)  from cve_info where updated_time > datetime('now','-7 days') group by danger_level having count(*)>1"
        #sql1 = "select * from cve_info where [updated_time]>= updated_time('now', 'localtime',  'start of day')"
        try:
            cursor.execute(sql)
            info1 = cursor.fetchall()
            today = datetime.datetime.now().weekday() + 1
            print(today)
            return str(info1)

        except Exception as e:
            print(e)
    else:

        return  "今天记得查看哦"