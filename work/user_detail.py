# coding=utf-8
import time
import re
import codecs
from selenium import webdriver
import work.reClass
import work.user_data
import work._database_
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
#设置chrome浏览器无界面模式
chrome_options.add_argument('--no-sandbox')#解决DevToolsActivePort文件不存在的报错
chrome_options.add_argument('window-size=1920x1080') #指定浏览器分辨率
chrome_options.add_argument('--disable-gpu') #谷歌文档提到需要加上这个属性来规避bug
chrome_options.add_argument('--hide-scrollbars') #隐藏滚动条, 应对一些特殊页面
chrome_options.add_argument('blink-settings=imagesEnabled=false') #不加载图片, 提升速度
chrome_options.add_argument('--headless') #浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
chrome_options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" #手动指定使用的浏览器位置
chrome_driver = 'G:\chrome\chromedriver_win32\chromedriver'
chrome = webdriver.Chrome(options=chrome_options,executable_path=chrome_driver)
_db = work._database_.DbClass()
_re = work.reClass.Re()
_re = work.reClass.Re()
#登录
def LoginWeibo(username, password):
    try:
        # 输入用户名/密码登录
        print(u'准备登陆')
        chrome.get("https://weibo.com/")
        # chrome.maximize_window()
        time.sleep(10)  # 等待页面载入
        elem_user = chrome.find_element_by_id('loginname')
        elem_user.clear()
        elem_user.send_keys(username)  # 用户名
        elem_pwd = chrome.find_element_by_class_name('password').find_element_by_name('password')
        elem_pwd.clear()
        elem_pwd.send_keys(password)  # 密码
        elem_rem = chrome.find_element_by_id("login_form_savestate")
        elem_rem.click()             #记住登录状态
        elem_sub = chrome.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a/span')
        elem_sub.click()  # 点击登陆
        cookie = chrome.get_cookies()
        time.sleep(1)
        print (cookie)
        print(u'登陆成功...')
    except Exception as e:
        print("Error: ", e)
def get_data(user_id):
    try:
        insert_list = []
        print (u'准备访问用户'+user_id +'\n')
        chrome.get("http://weibo.com/" + user_id)
        time.sleep(0.5)
        # 用户id
        print (u'用户id: ' + user_id)
        insert_list.append(user_id)
        # 昵称
        user_name = chrome.find_element_by_xpath("//div[@class='pf_username']")
        str_name = user_name.text.split(" ")
        u_name = str_name[0]  # 空格分隔 取第一个值
        print (u'昵称: ' + u_name)
        insert_list.append(u_name)
        # 简介
        user_intro = chrome.find_element_by_xpath("//div[@class='pf_intro']")
        str_intro = user_intro.text.split(" ")
        u_intro = str_intro[0]  # 空格分隔 取第一个值
        print (u'简介: ' + u_intro)
        insert_list.append(u_intro)
        # 关注数
        try:
            str_fw = chrome.find_element_by_xpath("//td[@class='S_line1'][1]/a/strong")
        except:
            str_fw = chrome.find_element_by_xpath("//td[@class='S_line1'][1]/strong")
        fw_count = _re.number(str_fw.text)
        print (u'关注数: ' + str(fw_count))
        insert_list.append(int(fw_count))

        # 粉丝数
        try:
            str_fans = chrome.find_element_by_xpath("//td[@class='S_line1'][2]/a/strong")
        except:
            str_fans = chrome.find_element_by_xpath("//td[@class='S_line1'][2]/strong")
        fans_count = _re.number(str_fans.text)
        print (u'粉丝数: ' + str(fans_count))
        insert_list.append(int(fans_count))

        # 微博数
        try:
            str_wb = chrome.find_element_by_xpath("//td[@class='S_line1'][3]/a/strong")
        except:
            str_wb = chrome.find_element_by_xpath("//td[@class='S_line1'][3]/strong")
        wb_count = _re.number(str_wb.text)
        print(u'微博数: ' + str(wb_count))
        insert_list.append(int(wb_count))
        # 微博认证
        try:
            str_ver = chrome.find_element_by_xpath("//div[@class='verify_area W_tog_hover S_line2'][1]/p[2]")
            user_ver = str_ver.text
        except:
            user_ver = '无'
        finally:
            print(u'微博认证: ' + user_ver)
            insert_list.append(user_ver)
         # 详情
        str_detail = chrome.find_elements_by_xpath("//div[@class='WB_innerwrap'][1]/div/div/ul/li")
        str_detail = list(str_detail)
        str_de = ''
        for i in range(1,len(str_detail)+1):
            try:
                details = chrome.find_element_by_xpath("//div[@class='WB_innerwrap'][1]/div/div/ul/li[{}]/span[2]".format(i))
                str_de = str_de +" "+ str(details.text)
            except:
                pass
        print(u"详情：" + str_de)
        insert_list.append(str_de)
        print(insert_list)
        return insert_list
    except :
        insert_list = ['无效数据','','',0,0,0,'','']
        print(insert_list)
        return insert_list
    finally:
        print (user_id+u' 完成!\n')
def insert_data(data):
    _db.connectDatabase()
    sql = "insert into userdetail_data(user_id,user_name,introduction,follow_count,fans_count,wb_count,verified,detail) values (%s,%s,%s,%s,%s,%s,%s,%s)"
    _db.executemany(sql,data)
    _db.close()

if __name__ == '__main__':
    username = '18742509891'  # 登录用户名
    password = 'wb19940207'  # 密码
    id_list = work.user_data.getid_list() #用户id列表
    LoginWeibo(username, password)  # 登陆微博
    # print(type(id_list),type(id_list[9]),id_list)
    u_list = []
    for i in range(0,len(id_list)):
        print(i)
        if i % 10 == 0 and i >= 10:
            insert_data(u_list)
            u_list = []
            time.sleep(3)
            u_data = get_data(str(id_list[i]))
            u_list.append(tuple(u_data))
        else:
            u_data = get_data(str(id_list[i]))
            u_list.append(tuple(u_data))
    chrome.close()
