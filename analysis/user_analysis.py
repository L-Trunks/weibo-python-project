import nltk
import sqlalchemy
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import work._database_
import work.reClass
import pymysql
import sys
import re
from wordcloud import WordCloud
import jieba
from sqlalchemy import create_engine
import analysis.blog_analysis
_db = work._database_.DbClass()
_re = work.reClass.Re()
_db.connectDatabase()

# userdetail_data数据3499条，无效数据79条

def getUser_data():
    sql = 'select * from userdetail_data'
    user_data = analysis.blog_analysis.pandas_read(sql)
    return user_data

def getbinpicture():
    user = getUser_data()
    # 根据地区分为不同的dataframe
    bei_count = user[user['detail'].str.contains('北京')]
    shang_count = user[user['detail'].str.contains('上海')]
    jiang_count = user[user['detail'].str.contains('江苏')]
    guang_count = user[user['detail'].str.contains('广东')]
    shan_count = user[user['detail'].str.contains('山东')]
    liao_count = user[user['detail'].str.contains('辽宁')]
    he_count = user[user['detail'].str.contains('河南')]
    si_count = user[user['detail'].str.contains('四川')]
    # 取补集，即其他地区
    other = user.append(bei_count)
    other = other.append(shang_count)
    other = other.append(jiang_count)
    other = other.append(guang_count)
    other = other.append(shan_count)
    other = other.append(liao_count)
    other = other.append(he_count)
    other = other.append(si_count)
    other = other.drop_duplicates(subset=['detail', 'user_name'], keep=False)
    labels = ['北京', '上海', '江苏', '广东', '山东', '辽宁', '河南', '四川','其他']
    number = [bei_count.user_name.count(), shang_count.user_name.count(),jiang_count.user_name.count(),
              guang_count.user_name.count(),shan_count.user_name.count(),liao_count.user_name.count(),
              he_count.user_name.count(),si_count.user_name.count(),other.user_name.count()]
    number = np.array(number)  # nparray类型
    plt.pie(number, labels=labels, autopct='%1.1f%%')
    plt.axis('equal')
    plt.legend()
    plt.show()
    # 根据学历
    u_count = user[user['detail'].str.contains('大学')]  # 本科及以上
    u_other = user.append(u_count)
    u_other = u_other.drop_duplicates(subset=['detail', 'user_name'], keep=False)  # 其他，可能未填写
    u_labels = ['本科及以上', '其他']
    u_number = [u_count.user_name.count(), u_other.user_name.count()]
    u_number = np.array(u_number)
    plt.pie(u_number, labels=u_labels, autopct='%1.1f%%')
    plt.axis('equal')
    plt.legend()
    plt.show()
    # 写入excel,根据地区分布
    writer = pd.ExcelWriter('E://univisity//Python\project//bigproject//excel//user.xlsx')
    bei_count.to_excel(writer, sheet_name='北京')
    shang_count.to_excel(writer, sheet_name='上海')
    jiang_count.to_excel(writer, sheet_name='江苏')
    guang_count.to_excel(writer, sheet_name='广东')
    shan_count.to_excel(writer, sheet_name='山东')
    liao_count.to_excel(writer, sheet_name='辽宁')
    he_count.to_excel(writer, sheet_name='河南')
    si_count.to_excel(writer, sheet_name='四川')
    other.to_excel(writer, sheet_name='其他')
    writer.save()
    writer.close()

def getword():
    user = getUser_data()
    word_list = ''.join(user['detail'])
    word_list = _re.Chinese(word_list)
    # 去除标签
    word_list = word_list.replace(re.findall('[简介]+',word_list)[0], '')
    word_list = word_list.replace(re.findall('[标签]+',word_list)[0], '')
    word_list = word_list.replace(re.findall('[Lv]+',word_list)[0], '')
    word_list = word_list.replace(re.findall('[年]+',word_list)[0], '')
    word_list = word_list.replace(re.findall('[月]+',word_list)[0], '')
    word_list = word_list.replace(re.findall('[日]+',word_list)[0], '')
    word_list = word_list.replace(re.findall('[公司]+',word_list)[0], '')
    word_list = word_list.replace(re.findall('[其他]+',word_list)[0], '')
    word_list = word_list.replace(re.findall('[个性域名]+',word_list)[0], '')
    word_list = word_list.replace(re.findall('[毕业]+',word_list)[0], '')
    word_count = ' '.join(jieba.cut(word_list))
    wordcloud = WordCloud(font_path=" C:\\Windows\\Fonts\\STXINGKA.TTF",
                          background_color="black", width=600,
                          height=300, max_words=400, min_font_size=8).generate(word_count)
    image = wordcloud.to_image()
    image.show()
if __name__ == "__main__":
    # getUser_data()
    # getbinpicture()
    getword()