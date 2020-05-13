import concurrent
import os
from concurrent.futures import ThreadPoolExecutor
import time
import requests
from bs4 import BeautifulSoup
# _*_ coding:utf-8 _*_  #声明程序的编写字符
import requests #导入requests库
import json #导入json库

import work._database_
import work.reClass
_db = work._database_.DbClass()
_re = work.reClass.Re()
_db.connectDatabase()
sql = "insert into user_data(username,user_id,follow_count,follower_count,verified,introduction) values (%s,%s,%s,%s,%s,%s)"

def getid_list():
    id_sql = "select user_id from comment_data"
    res = _db.select(id_sql)
    id_list = []
    for i in res:
        id = _re.number(str(i))
        id_list.append(int(id))
    id_list = list(set(id_list))
    print('用户id数为:'+str(len(id_list)))
    return id_list
def getrequest(url):
    try:
        header = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'
        }
        res = requests.get(url,headers=header,timeout=20)
        data = json.loads(res.text)
        return data['data']['userInfo']
    except:
        return 'error'

def get_data():
    url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value={}'
    id_list = getid_list()
    for i in range(0, len(id_list)):
        insert_data = ['', '', '', '', '', '']
        try:
            data = getrequest(url.format(str(id_list[i])))
            insert_data[0] = str(data['screen_name'])
            insert_data[1] = str(data['id'])
            insert_data[2] = data['follow_count']
            insert_data[3] = data['followers_count']
            if data['verified']:
                insert_data[4] = data['verified_reason']
            else:
                insert_data[4] = '无'
            insert_data[5] = data['description']
        except:
            pass
        finally:
            _db.execute(sql, insert_data)
            print(i)
if __name__ == "__main__":
    get_data()