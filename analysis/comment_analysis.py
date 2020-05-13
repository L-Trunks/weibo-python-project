import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import work._database_
import work.reClass
import analysis.blog_analysis

_db = work._database_.DbClass()
_re = work.reClass.Re()
# _db.connectDatabase()

def getcomment():
    u_sql = 'select b.title,c.article,c.like_count,c.follow_count,c.follower_count,c.username,c.verified,c.introduction from comment_data c left outer join blog_data b on c.mid = b.mid where c.like_count > 100 '
    # comment_data = _db.select(u_sql)
    c_table = analysis.blog_analysis.pandas_read(u_sql)
    return c_table

def getpicture():
    data = getcomment()
    data_count = [data['like_count'],data['follower_count']]
    l = np.array(data_count).tolist()
    count_list = []
    for i in range(0,len(l[0])):
        temp = [l[0][i],l[1][i]]
        count_list.append(temp)
    #去重
    new_list = [list(t) for t in set(tuple(y) for y in count_list)]
    # print(len(count_list),count_list)
    # print(len(new_list),new_list)
    for i in range(0, len(new_list)):
        # 点赞数为x轴，粉丝数为y轴
        plt.scatter(new_list[i][0], new_list[i][1],
                    c='r', s=10, alpha=0.5)
    plt.show()
def getbingpicture():
    data = getcomment()
    ver_count = data[data['verified'] != '无'].article.count()
    nover_count = data[data['verified'] == '无'].article.count()
    labels = ['认证用户', '非认证用户']
    number = [ver_count, nover_count]
    number = np.array(number)  # nparray类型
    plt.pie(number, labels=labels, autopct='%1.1f%%')
    plt.axis('equal')
    plt.legend()
    plt.show()


def writeExcel():
    data = getcomment()
    s_data = data[data['like_count'] < 500]
    hotdata = data[data['like_count'] > 500]
    writer = pd.ExcelWriter('E://univisity//Python\project//bigproject//excel//comment.xlsx')
    hotdata.to_excel(writer, sheet_name='热门评论')
    s_data.to_excel(writer, sheet_name='次热门评论')
    writer.save()
    writer.close()
if __name__ == '__main__':
    # getuser()
    #  getpicture()
    # writeExcel()
    getbingpicture()
