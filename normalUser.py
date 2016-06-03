# -*- coding: utf-8 -*-
"""
获取所有用户的id，并查找最多发一条微博的用户id
"""

import MySQLdb

'''定义数据库连接'''
def get_mysql_conn():
    conn = MySQLdb.connect(host="127.0.0.1", db="weibo",
                           user="root", passwd="root",charset="utf8")
    conn.autocommit(False)
    cursor = conn.cursor()
    cursor.execute("SET NAMES 'utf8mb4'")
    cursor.close()
    return conn

'''获取所有用户的ID'''
def get_users():    
    conn = get_mysql_conn()
    cursor = conn.cursor()
    sql = "SELECT id FROM %s" % u_table
    cursor.execute(sql)
    results = cursor.fetchall()
    u_list = []
    for i in results:
        u_list.append(i[0])
    cursor.close()
    return(u_list)

'''筛选出至少发布一条微博的用户ID'''
def select_users(user_list_all):    
    conn = get_mysql_conn()
    cursor = conn.cursor()
    u_list = []  # 第一列是user_id，第二列是发布微博的数量
    for user in user_list_all:
        sql = "SELECT * FROM %s where user_id=%s" % (mes_table,user)
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results) > 1:
            temp = (user,len(results))
            u_list.append(temp)
    return(u_list)

def new_table(user_list):
    conn = get_mysql_conn()
    cursor = conn.cursor()
    sql1 = "DROP TABLE IF EXISTS %s" % user_table
    cursor.execute(sql1)  
    sql2 = "CREATE TABLE %s (user_id bigint primary key, count_weibo int)" % user_table
    cursor.execute(sql2)
    for item in user_list:
        sql3 = "INSERT into %s(user_id,count_weibo) values('%s','%s')" % (user_table,item[0],item[1])
        cursor.execute(sql3)
    conn.commit()
    cursor.close()
'''
# 第一组用户和内容
user_table = 'selectedUser'
mes_table = 'message'
u_table = 'user'
'''
# 第二组用户和内容
user_table = 'selectedUser1'
mes_table = 'message1'
u_table = 'user1'

def main():
    user_list_all = get_users()
    # print user_list_all
    # print type(user_list_all)
    user_list = select_users(user_list_all)
    new_table(user_list)
    # 写入txt
    f = open((user_table+'.txt'),'w')
    for item in user_list:
        f.write(str(item)+'\n')
    f.close()

if  __name__=="__main__":
    main()


