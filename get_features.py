#coding=utf-8
import MySQLdb,datetime
import spam_words
import arff

def get_mysql_conn():
    conn = MySQLdb.connect(host="127.0.0.1", db="weibo",
                           user="root", passwd="root",charset="utf8")
    conn.autocommit(False)
    cursor = conn.cursor()
    cursor.execute("SET NAMES 'utf8mb4'")
    cursor.close()
    return conn

temp = spam_words.spam_words.values()
temp = temp[0].split("OR")
spam_list = []
for item in temp:
    spam_list.append(item.strip())
num_list=['0','1','2','3','4','5','6','7','8','9']

def feature_from_list(li1):
##    print li1
    fea1=int(max(li1))
    fea2=int(min(li1))
    fea3=float(sum(li1))/float(len(li1))
    li2=sorted(li1)
##    print li2
    if len(li2)%2==1:
        fea4=li2[len(li2)/2]
    else:
        fea4=(li2[len(li2)//2-1]+li2[len(li2)//2])/2.0
    return(fea1,fea2,fea3,fea4)

def analyse_time_list(time_list1):
    time_list2=sorted(time_list1)
    diff_list=[]
    for i in range(len(time_list2)-1):
        diff_list.append(time_list2[i+1]-time_list2[i])
    va1,va2,va3,va4=feature_from_list(diff_list)
    return(va1,va2,va3,va4)


def get_content_features(u_id):
    conn=get_mysql_conn()
    cursor=conn.cursor()
    sql="select text,retweet_count,original_message_id,UNIX_TIMESTAMP(created_at),id from %s where user_id=%s" % (mes_table,u_id)
    cursor.execute(sql)
    results=cursor.fetchall()
    spam_num=0
    re_num=0
    url_num=0
    list1=[]
    list2=[]
    list3=[]
    list4=[]
    list5=[]
    list6=[]
    list7=[]
    list8=[]
    tota=len(results)
    time_list=[]
    for result in results:
        time_list.append(int(result[3]))
        content=result[0]
        num_hash=content.count('#')
        num_url=content.count('http://')
        num_char=len(content)
        hash_per=float(num_hash)/float(num_char)
        url_per=float(num_url)/float(num_char)
        num_mention=content.count('@')
        num_retweet=int(result[1])
        num_numstr=0
        for num_str in num_list:
            num_numstr+=content.count(num_str)
        num_spam=0  
        for spam in spam_list:
            num_spam+=content.count(spam)
        list1.append(hash_per)
        list2.append(url_per)
        list3.append(num_char)
        list4.append(num_url)
        list5.append(num_hash)
        list6.append(num_numstr)
        list7.append(num_mention)
        list8.append(num_retweet)
        if num_spam>0:
            spam_num+=1
        if result[2]>0:
            re_num+=1
        if num_url>0:
            url_num+=1
    cursor.close()
    conn.close()
    f1,f2,f3,f4=feature_from_list(list1)
    f5,f6,f7,f8=feature_from_list(list2)
    f9,f10,f11,f12=feature_from_list(list3)
    f13,f14,f15,f16=feature_from_list(list4)
    f17,f18,f19,f20=feature_from_list(list5)
    f21,f22,f23,f24=feature_from_list(list6)
    f25,f26,f27,f28=feature_from_list(list7)
    f29,f30,f31,f32=feature_from_list(list8)
    f33=float(spam_num)/float(tota)
    f34=float(re_num)/float(tota)
    f35=float(url_num)/float(tota)
    uf6=re_num
    uf8,uf9,uf10,uf11=analyse_time_list(time_list)
    cf_list=[f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16,f17,f18,f19,f20,f21,f22,f23,f24,f25,f26,f27,f28,f29,f30,f31,f32,f33,f34,f35,uf6,uf8,uf9,uf10,uf11]
    return(cf_list)

def count_days(date1):
    now = datetime.datetime.now()
    days=(now-date1).days-240
    return(days)

def get_user_features(u_id):
    conn=get_mysql_conn()
    cursor=conn.cursor()
    sql="select follower_count,followee_count,message_count,created_at,screen_name from %s where id=%s" % (u_table,u_id)
    cursor.execute(sql)
    results=cursor.fetchall()
    uf1=int(results[0][0])
    uf2=int(results[0][1])
    if uf2 == 0:
        uf3 = 0
    else:
        uf3=float(uf1)/float(uf2)
    uf4=int(results[0][2])
    uf5=count_days(results[0][3])

    sname=results[0][4]
    num_spam=0  
    for spam in spam_list:
        num_spam+=sname.count(spam)
    uf7=num_spam
    cursor.close()
    cursor1=conn.cursor()
    sql1="SELECT DATE_FORMAT(created_at, '%s') as m, count(*) as so_count FROM %s where user_id=%s GROUP BY m ORDER BY m" % ('%Y-%m-%d',mes_table,u_id)
##    print sql1
    cursor1.execute(sql1)
    results1=cursor1.fetchall()
    day_count_list=[]
    for result1 in results1:
        day_count_list.append(int(result1[1]))
    cursor1.close()
    cursor2=conn.cursor()
    sql2="SELECT DATE_FORMAT(created_at, '%s') as m, count(*) as so_count FROM %s where user_id=%s GROUP BY m ORDER BY m" % ('%x %v',mes_table,u_id)
    cursor2.execute(sql2)
    results2=cursor2.fetchall()
    week_count_list=[]
    for result2 in results2:
        week_count_list.append(int(result2[1]))
    cursor2.close()
    conn.close()
    uf12,uf13,uf14,uf15=feature_from_list(day_count_list)
    uf16,uf17,uf18,uf19=feature_from_list(week_count_list)
    uf_list=[uf1,uf2,uf3,uf4,uf5,uf7,uf12,uf13,uf14,uf15,uf16,uf17,uf18,uf19]
    return(uf_list)

def get_users():
    
    conn=get_mysql_conn()
    cursor=conn.cursor()
    sql="SELECT user_id FROM %s" % user_table
    cursor.execute(sql)
    results=cursor.fetchall()
    u_list=[]
    for i in results:
        u_list.append(i[0])
    cursor.close()
    return(u_list)

def main(data3):
    user_list=get_users()  # 读取至少发布过一条微博的用户ID
    count_selectedUser=0  # 计算至少发布过一条微博的用户数目
    for user in user_list:
        f_list1=get_content_features(user)
        f_list2=get_user_features(user)
        count_selectedUser+=1    
        f_list3=f_list1+f_list2
        temp = [user]+f_list3
        print temp
        data3.append(temp)
    print count_selectedUser
    return data3

if  __name__=="__main__":
    data = []
    for i in range(2):
        if i==0:
            user_table = 'selectedUser'
            mes_table = 'message'
            u_table = 'user'
            data = main(data)   # 第一组用户和内容
        else:
            user_table = 'selectedUser1'
            mes_table = 'message1'
            u_table = 'user1'
            data = main(data)   # 第二组用户和内容
    arff.dump('total.arff',data,relation="weibo",
                  names=['user_id','hash_per_max','hash_per_min','hash_per_mean','hash_per_median',
                         'url_per_max','url_per_min','url_per_mean','url_per_median',
                         'num_char_max','num_char_min','num_char_mean','num_char_median',
                         'num_url_max','num_url_min','num_url_mean','num_url_median',
                         'num_hash_max','num_hash_min','num_hash_mean','num_hash_median',
                         'num_numstr_max','num_numstr_min','num_numstr_mean','num_numstr_median',
                         'num_mention_max','num_mention_min','num_mention_mean','num_mention_median',
                         'num_retweet_max','num_retweet_min','num_retweet_mean','num_retweet_median',
                         'spam_avg','re_avg','url_avg','re_num',
                         'time_interval_max','time_interval_min','time_interval_mean','time_interval_median',
                         'follower_count','followee_count','follower_per','message_count','created_days','spam_num',
                         'day_count_max','day_count_min','day_count_mean','day_count_median',
                         'week_count_max','week_count_min','week_count_mean','week_count_median'])


