#!/usr/bin/env python
# coding:UTF-8
import pymysql
import sys


class DbClass:
    # 构造函数
    def __init__(self, host='127.0.0.1', port=3306, user='root',
                 passwd='root', db='python_webo', charset='utf8mb4'):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db
        self.charset = charset
        self.conn = None
        self.cur = None

    # 连接数据库
    def connectDatabase(self):
        try:
            self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db,
                                        charset=self.charset)
            self.cur = self.conn.cursor()
            print("数据库连接成功")
        except:
            return False

        return True

    # 关闭数据库
    def close(self):
        # 如果数据打开，则关闭；否则没有操作
        if self.conn and self.cur:
            self.cur.close()
            self.conn.close()
            print("数据库连接已关闭")
        return True

    # 执行数据库的sq语句
    def execute(self, sql, params=None):
        # 连接数据库
        try:
            if self.conn and self.cur:
                # 正常逻辑，执行sql，提交操作
                rowcount = self.cur.execute(sql, params)
                print('操作成功')
                self.conn.commit()
        except:
            # self.close()
            return False
        return rowcount
    def select(self, sql, params=None):
        # 连接数据库
        try:
            if self.conn and self.cur:
                # 正常逻辑，执行sql，提交操作
                self.cur.execute(sql, params)
                results = self.cur.fetchall()
                self.conn.commit()
        except:
            # self.close()
            return False
        return results

    # 执行数据库的sq语句,主要用来做批量插入
    def executemany(self, sql, params=None):
        # 连接数据库
        try:
            if self.conn and self.cur:
                # 正常逻辑，执行sql，提交操作
                rowcount = self.cur.executemany(sql, params)
                print(rowcount)
                self.conn.commit()
        except:
            # self.close()
            return False
            return rowcount


if __name__ == '__main__':
    db = DbClass()
    sql = "insert into blog_data(title,mid,good_count,comment_count,report_count,article,sign,m_environment,look_count,m_from,m_date) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    list = ('上海出台 涉性侵犯罪人员从业限制 意见 除教师医生外保安门卫也需审查', '4377397434080573', 3059, 432, 1247, '上海出台 涉性侵犯罪人员从业限制 意见 除教师医生外保安门卫也需审查 日 上海市 家单位会签并出台了 关于建立涉性侵害违法犯罪人员从业限制制度的意见 这是全国首个省级涉性侵害违法犯罪人员从业限制制度 除了对教师 医生 教练 保育员等直接对未成年人负有特殊职责的工作人员进行审查 全文', '上海出台 涉性侵犯罪人员从业限制 意见 除教师医生外保安门卫也需审查', '微博 weibo.com', '', '', '')
    db.connectDatabase()
    result = db.execute(sql, list)
    db.close()
    #
    # sql = """
    #     CREATE TABLE person_data (
    #          id int(10)  primary key auto_increment,
    #          微博标题  varchar(50) NOT NULL,
    #          微博id  varchar(50) not null,
    #          点赞数  varchar(50),
    #          评论数  varchar(50),
    #          转发数  varchar(50),
    #          内容  varchar(1000),
    #          标签 varchar(20),
    #          发博环境  varchar(30),
    #          浏览量  varchar(50),
    #          来源  varchar(50),
    #          时间  varchar(50)
    #          )
    #         """