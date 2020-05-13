#!/usr/bin/python3
import pymysql
# 打开数据库连接
db = pymysql.connect("localhost", "root", "root", "python_webo")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
# 使用 execute() 方法执行 SQL，如果表存在则删除
cursor.execute("DROP TABLE IF EXISTS userDetail_data")
# 使用预处理语句创建表
sql = """

    CREATE TABLE userDetail_data (
         id int(10)  primary key auto_increment,
         user_id  varchar(50),
         user_name varchar(50),
         introduction varchar(500),
         follow_count int(50),
         fans_count int(10),
         wb_count int(10),
         verified varchar(100),
         detail varchar(500)
         )
        """
cursor.execute(sql)
# 关闭数据库连接
db.close()