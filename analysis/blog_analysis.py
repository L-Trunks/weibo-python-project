import sqlalchemy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import work._database_
import work.reClass
import pymysql
import sys
from sqlalchemy import create_engine
# 绘图支持中文
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']

_db = work._database_.DbClass()
_re = work.reClass.Re()
_db.connectDatabase()
#获取点赞，评论，转发数
def getNotice():
   notice_sql = 'select good_count,comment_count,report_count from blog_data limit 500'
   notice = list(_db.select(notice_sql))
   print(len(notice), notice)
   notice = [[i, j, k] for i, j, k in notice]
   newNotice = []
   for i in range(0, len(notice)):
      if notice[i][0] != '' and notice[i][1] != '' and notice[i][2] != '':
         newNotice.append(notice[i])
   print(newNotice)
   return newNotice
#
def getscatter():
   test = getNotice()
   for i in range(0, len(test)):
      # 点赞数为x轴，评论数为y轴
      plt.scatter(test[i][0], test[i][1],
                  c='r', s=10, alpha=0.5)
      # #点赞数为x轴，转发数为y轴
      plt.scatter(test[i][0], test[i][2],
                  c='g', s=10, alpha=0.5)
      # #评论数为x轴，转发数为y轴
      plt.scatter(test[i][1], test[i][2],
                  c='b', s=10, alpha=0.5)
   plt.show()
#
def pandas_read(_sql):
   _db.close()
   try:
      engine = create_engine('mysql+pymysql://root:root@localhost:3306/python_webo?charset=utf8mb4')
   except sqlalchemy.exc.OperationalError as e:
      print('Error is ' + str(e))
      sys.exit()
   except sqlalchemy.exc.InternalError as e:
      print('Error is ' + str(e))
      sys.exit()
   p_table = pd.read_sql(_sql,con=engine)
   return p_table
def bin_Picture(data):
   #评论平均数
   nm = data['comment_count'].mean(axis=0)
   print(nm)
   small_comment = data[data.comment_count<800].comment_count.count()
   model_comment = data[data.comment_count<1600].comment_count.count() - small_comment
   large_comment = data[data.comment_count<2400].comment_count.count() - (small_comment+model_comment)
   nm_comment = data[data.comment_count<3200].comment_count.count() - (small_comment+model_comment+large_comment)
   max_comment = data[data.comment_count>3200].comment_count.count()
   labels = ['<800', '800-1600', '1600-2400', '2400-3200', '>3200']
   number = [small_comment,model_comment,large_comment,nm_comment,max_comment]
   number = np.array(number) # nparray类型
   plt.pie(number, labels=labels, autopct='%1.1f%%')
   plt.axis('equal')
   plt.legend()
   plt.show()

def word_count():
   word_sql = 'select * from blog_data'
   word_data = pandas_read(word_sql)
   night = word_data[word_data['title'].str.contains('夜读')]
   war = word_data[word_data['title'].str.contains('贸易战')]
   mei = word_data[word_data['title'].str.contains('中美')]
   zhong = word_data[word_data['title'].str.contains('中国')]
   food = word_data[word_data['title'].str.contains('美食')|word_data['article'].str.contains('美食')]
   # 取补集，即其他
   other = word_data.append(night)
   other = other.append(war)
   other = other.append(mei)
   other = other.append(zhong)
   other = other.append(food)
   other = other.drop_duplicates(subset=['title', 'article'], keep=False)
   writer = pd.ExcelWriter('E://univisity//Python\project//bigproject//excel//blog.xlsx')
   night.to_excel(writer, sheet_name='夜读')
   war.to_excel(writer, sheet_name='贸易战')
   mei.to_excel(writer, sheet_name='中美关系')
   zhong.to_excel(writer, sheet_name='时事')
   food.to_excel(writer,  sheet_name='美食')
   other.to_excel(writer,  sheet_name='其他')
   writer.save()
   writer.close()
   # 绘制饼状图
   night_count = night.title.count()
   war_count = war.title.count()
   mei_count = mei.title.count()
   zhong_count = zhong.title.count()
   food_count = food.title.count()
   other_count = other.title.count()
   labels = ['夜读', '贸易战', '中美关系', '时事', '美食','其他']
   number = [night_count, war_count, mei_count, zhong_count, food_count,other_count]
   number = np.array(number)  # nparray类型
   plt.pie(number, labels=labels, autopct='%1.1f%%')
   plt.axis('equal')
   plt.legend()
   plt.show()

if __name__=="__main__":
   #散点图
   # getscatter()
   # sql = 'select * from blog_data limit 5000'
   # blog_data = pandas_read(sql)
   # print(type(blog_data))
   # bin_Picture(blog_data)
   word_count()