
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
sql = "insert into blog_data(title,mid,good_count,comment_count,report_count,article,sign,m_environment,look_count,m_from,m_date) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
def getrequest(url,page):
    time.sleep(1)
    s = requests.session()
    s.keep_alive = False
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
        'Cookie': 'SCF=AgJlxQF1EbT-RlxfUFrRbaK7ZDxg847ZLsKVjq69XPVCRAaPGc5L2QTLkodxdrPyykJZyAep6Mq5nQ33wGEMONU.; SUB=_2A25x9yA0DeRhGeVG6VAX8i3IyDmIHXVTGEB8rDV6PUJbktANLUrykW1NT6yqG5TbEQYTeB-QbFftL7fZpbnetYe4; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Whi0rzFu6VOCravdDw49_5B5JpX5KzhUgL.FoeReozceoeXe0-2dJLoI7YLxKBLBonLB.9-MrHVINet; SUHB=0OMkEQIU6F_pEN; _T_WM=85841206785; MLOGIN=1; WEIBOCN_FROM=1110006030; XSRF-TOKEN=e0b479; M_WEIBOCN_PARAMS=oid%3D4378799783067738%26luicode%3D10000011%26lfid%3D2304132803301701_-_WEIBO_SECOND_PROFILE_WEIBO%26fid%3D2304132803301701_-_WEIBO_SECOND_PROFILE_WEIBO%26uicode%3D10000011'}
    url = url+str(page)
    data = s.get(url,headers=header,timeout=10)  # 通过requests的get方法请求
    return data
def get_blog(data):
    if data.content:
        data = json.loads(data.text)  # 解析json数据
        for i in range(0, len(data['data']['cards'])):
            if data['data']['cards'][i]['card_type']==9:
                text = data['data']['cards'][i]['mblog']
                return text
def get_detail(blog):
    insert_data = ['','','','','','','','','','','']
    try:
        if _re.findTitle(blog['text']):
            insert_data[0] = _re.findTitle(blog['text'])
        elif blog['page_info']:
            if blog['page_info']['page_title']:
                insert_data[0] = blog['page_info']['page_title']
            elif blog['obj_ext']:
                insert_data[0] = blog['page_info']['content2']
            else:
                insert_data[0] = blog['page_info']['content1']
        else:
            insert_data[0] = blog['mid']
        insert_data[1] = blog['id']
        insert_data[2] = blog['attitudes_count']
        insert_data[3] = blog['comments_count']
        insert_data[4] = blog['reposts_count']
        insert_data[5] = _re.article(blog['text'])
        if _re.findSign(blog['text']):
            insert_data[6] = _re.findTitle(blog['text'])
        elif blog['page_info']:
            if blog['page_info']['page_title']:
                insert_data[6] = blog['page_info']['page_title']
            else:
                insert_data[6] = '无'
        else:
            insert_data[6] = '无'
        insert_data[7] = blog['source']
        if blog['page_info']:
            insert_data[9] = blog['page_info']['content1']
        else:
            insert_data[9] = '无法获取'
        insert_data[10] = blog['created_at']
        if blog['page_info']:
            insert_data[8] = blog['page_info']['content2']
        elif blog['obj_ext']:
            insert_data[8] = blog['obj_ext']
        else:
            insert_data[8] = '无法获取'
    except:
        pass
        # insert_data = ['error','error','error','error','error','error','error','error','error','error','error']
    return tuple(insert_data)



def get_data(url,start,end):
    # insert_list = []
    for i in range(start, end):  # 遍历页数
        if i % 10 == 0 and i >= 10:
            time.sleep(15)
            data = getrequest(url, i)
            blog = get_blog(data)
            insert_data = get_detail(blog)
            _db.execute(sql, insert_data)
            print(i)
            # insert_list.append(insert_data)
        else:
            data = getrequest(url, i)
            blog = get_blog(data)
            insert_data = get_detail(blog)
            _db.execute(sql, insert_data)
            print(i)
            # insert_list.append(insert_data)

#截至6.2晚九点人民日报的微博
# url = 'https://m.weibo.cn/api/container/getIndex?containerid=2304132803301701_-_WEIBO_SECOND_PROFILE_WEIBO&page_type=03&page='
# get_data(url,7494,9800)
_db.close()
# tex = getrequest(url,1)
# print(get_blog(tex))