import re

class Re:
    #返回微博标签
    def findSign(self,str):
        res = re.findall(r"#(.+?)#",str)
        try:
            return ' '.join(res)
        except:
            return None

    #返回微博标题
    def findTitle(self,str):
        try:
            text = re.match(r"【(.+?)】",str).group()
            return ' '.join(re.findall(u"([\u4e00-\u9fff“”]+)",text))
        except Exception as e:
            print("Error:" + e)
    #返回去除标签后的内容
    def article(self,str):
        try:
            return "".join(re.findall(u"([\u4e00-\u9fff“”，：。！@]+)",str))
        except Exception as e:
            print("Error:"+e)
    def number(self,str):
        try:
            return "".join(re.findall(u"([0-9]+)",str))
        except Exception as e:
            print("Error:" + e)
    #去重
    def removeRepeat(self,ls):
        try:
            ls = list(set(ls))
            new = []
            for i in ls :
                if len(i)!=0:
                    new.append(i)
            return new
        except Exception as e:
            print("Error:" + e)
    #中文
    def Chinese(self,s):
        try:
            return ''.join(re.findall(r'[\u4e00-\u9fa5a-zA-Z]+',s))
        except Exception as e:
            print('Error:'+e)
if __name__ == '__main__':
    test = Re()
    s = "【全文来了！《关于中美经贸磋商的中方立场》白皮书】转发传递，<a  href=https://m.weibo.cn/search?containerid=231522type%3D1%26t%3D10%26q%3D%23%E8%BF%99%E5%B0%B1%E6%98%AF%E4%B8%AD%E5%9B%BD%E6%80%81%E5%BA%A6%23&luicode=10000011&lfid=1076032803301701 data-hide=""><span class=surl-text>#这就是中国态度#</span></a>！ <a data-url=http://t.cn/Ai9yAh6 href=https://media.weibo.cn/article?object_id=1022%3A2309404378682297816755&extparam=lmid--4378682300708982&luicode=10000011&lfid=1076032803301701&id=2309404378682297816755 data-hide=""><span class='url-icon'><img style='width: 1rem;height: 1rem' src='https://h5.sinaimg.cn/upload/2015/09/25/3/timeline_card_small"
    t = test.findTitle(s)
    t1 = test.findSign(s)
    # t2 = test.article(s)
    print(t)
