import time,string
import pymysql
from jieba.analyse import extract_tags

def get_time():
    time_str= time.strftime("%Y{}%m{}%d{} %X")
    return time_str.format("年","月","日")



def get_conn():
    conn=pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="12345",
    db="cov"
)
    cursor=conn.cursor()
    return conn,cursor

def close_conn(conn,cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()





def query(sql,*args):
    conn, cursor = get_conn()
    cursor.execute(sql, args)
    res = cursor.fetchall()
    close_conn(conn, cursor)
    return res




def get_c1_data():
    sql = "SELECT SUM(confirm)," \
          "(SELECT suspect FROM history ORDER BY ds desc LIMIT 1)," \
          "sum(heal)," \
          "SUM(dead) " \
          "FROM details " \
          "WHERE update_time=(SELECT update_time FROM details ORDER BY update_time desc LIMIT 1)"
    res = query(sql)
    return res[0]


def get_c2_data():
    sql = "SELECT province," \
          "SUM(confirm) " \
          "FROM details " \
          "WHERE update_time=(SELECT update_time FROM details ORDER BY update_time DESC LIMIT 1) " \
          "GROUP BY province"
    res = query(sql)
    return res

def get_l1_data():
    sql = "SELECT ds,confirm,suspect,heal,dead from history"
    res = query(sql)
    return res

def get_l2_data():
    sql = "select ds,confirm_add,suspect_add from history"
    res = query(sql)
    return res

def get_r1_data():
    sql = "SELECT city,confirm " \
          "from " \
          "(SELECT city,confirm from details" \
          " WHERE update_time=(SELECT update_time FROM details ORDER BY update_time desc LIMIT 1) " \
          "and province not in ('湖北','北京','上海','天津','重庆') " \
           "UNION ALL " \
           "SELECT province as city, sum(confirm) as confirm FROM details " \
           "WHERE update_time=(SELECT update_time FROM details ORDER BY update_time desc LIMIT 1) " \
           "and province in ('湖北','北京','上海','天津','重庆') GROUP BY province) as a " \
            "ORDER BY confirm desc LIMIT 5"
    res=query(sql)
    return res

def get_r2_data():
    sql="SELECT content FROM jinri_hot ORDER BY id desc LIMIT 20"
    res=query(sql)
    return res


if __name__=="__main__":
    print(get_r2_data())