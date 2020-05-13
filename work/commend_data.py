import time
from bs4 import BeautifulSoup
# _*_ coding:utf-8 _*_  #声明程序的编写字符
import requests #导入requests库
import json #导入json库
import work._database_
import work.reClass


_db = work._database_.DbClass()
_re = work.reClass.Re()
_db.connectDatabase()
sql = "insert into comment_data(mid,comment_id,article,like_count,username,user_id,follow_count,follower_count,verified,introduction,m_date) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
#请求 返回json格式的数据
def getrequest(id,mid):
    time.sleep(1)
    s = requests.session()
    s.keep_alive = False
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
        'Cookie': 'SCF=AgJlxQF1EbT-RlxfUFrRbaK7ZDxg847ZLsKVjq69XPVCRAaPGc5L2QTLkodxdrPyykJZyAep6Mq5nQ33wGEMONU.; SUB=_2A25x9yA0DeRhGeVG6VAX8i3IyDmIHXVTGEB8rDV6PUJbktANLUrykW1NT6yqG5TbEQYTeB-QbFftL7fZpbnetYe4; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Whi0rzFu6VOCravdDw49_5B5JpX5KzhUgL.FoeReozceoeXe0-2dJLoI7YLxKBLBonLB.9-MrHVINet; SUHB=0OMkEQIU6F_pEN; _T_WM=85841206785; MLOGIN=1; WEIBOCN_FROM=1110006030; XSRF-TOKEN=e0b479; M_WEIBOCN_PARAMS=oid%3D4378799783067738%26luicode%3D10000011%26lfid%3D2304132803301701_-_WEIBO_SECOND_PROFILE_WEIBO%26fid%3D2304132803301701_-_WEIBO_SECOND_PROFILE_WEIBO%26uicode%3D10000011',
        'Refer': 'https://m.weibo.cn/detail/{}'.format(id)
    }
    url = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type=0'.format(id, mid)
    data = s.get(url,headers=header,timeout=10)  # 通过requests的get方法请求
    data = json.loads(data.text)
    return data['data']['data']
#数据处理
def get_comment(id,data):
    result_list = []
    for i in range(0, len(data)):
        insert_list = ['', '', '', '', '', '', '', '', '', '', '']
        insert_list[0] = id
        insert_list[1] = data[i]['id']
        insert_list[2] = _re.article(data[i]['text'])
        insert_list[3] = data[i]['like_count']
        insert_list[4] = data[i]['user']['screen_name']
        insert_list[5] = data[i]['user']['id']
        insert_list[6] = data[i]['user']['follow_count']
        insert_list[7] = data[i]['user']['followers_count']
        if data[i]['user']['verified']:
            insert_list[8] = data[i]['user']['verified_reason']
        else:
            insert_list[8] = '无'
        insert_list[9] = data[i]['user']['description']
        insert_list[10] = data[i]['created_at']
        result_list.append(tuple(insert_list))
    return result_list
def getdetail(id,mid):
    insert_data = getrequest(id,mid)
    insert_list = get_comment(id,insert_data)
    _db.executemany(sql,insert_list)

#爬取blog_data表内前400条数据的热门评论
if __name__ == '__main__':
    id_sql = 'select mid from blog_data limit 400'
    # getdetail('4379045812809325','4379045812809325')
    id_list = _db.select(id_sql)
    for i in id_list:
        s = _re.number(str(i))
        if s != '':
            getdetail(s, s)
    _db.close()