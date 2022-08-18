"""
用户脚本：睡前消息-马前卒工作室
需要提供URL列表生成函数get_urls()，以及文章解析函数parse_article()
"""
import re
import time
import random
import datetime
import platform
import requests
from requests.adapters import HTTPAdapter, Retry
from faker import Faker
from bs4 import BeautifulSoup


class GetURLs:
    """获取一段时间内睡前消息文章的URL列表"""

    def __init__(self):
        # 初始化feeddd源
        self.homepage_feeddd = 'https://api.feeddd.org/feeds/612320c451e2511a827a11d6'
        r_feeddd = requests.get(self.homepage_feeddd)
        self.soup_feeddd = BeautifulSoup(r_feeddd.text, 'xml')

        # 初始化搜狗源
        self.homepage_sogo = 'https://weixin.sogou.com/weixin'

        self.sess_sogo = requests.session()
        # 搜狗本身只需要user-agent即可访问，访问微信推文需要referer和cookie，这里为了方便集成在一起
        self.sess_sogo.headers = {'user-agent': Faker().user_agent(), 
                                  'referer': 'https://weixin.sogou.com/weixin?type=2&s_from=input&query='
                                    '%E7%9D%A1%E5%89%8D%E6%B6%88%E6%81%AF&ie=utf8&_sug_=n&_sug_type_=',
                                  'cookie': 'SUID=0C91AE272208990A000000005C7145DC; SUV=1550927324797555; '
                                    'ssuid=8275997946; LSTMV=241%2C183; LCLKINT=5135; IPLOC=CN3301; weixinIndexVisited=1; '
                                    'ABTEST=0|1654062326|v1; SNUID=67E1DE5770758F331506DFA470A2FCB2; JSESSIONID=aaaSeJsIn-ln9fmk-p6dy; '
                                    'ariaDefaultTheme=undefined'
                                 }
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        self.sess_sogo.mount('http://', adapter)
        self.sess_sogo.mount('https://', adapter)

    def __call__(self, length=5):
        url_list = []
        for l in range(length):
            date = datetime.date.today() - datetime.timedelta(days=l)
            if platform.system() == 'Windows':
                title = '睡前消息【%s】' % date.strftime('%Y-%#m-%#d')
            else:
                title = '睡前消息【%s】' % date.strftime('%Y-%-m-%-d')

            url = self.get_url_by_title_feeddd(title)
            if not url: # 若feeddd未获取到当日文章，则尝试通过搜狗搜索获取
                url = self.get_url_by_title_sogo(title)
            if url:     # 若最终得到当日文章的URL，则将其添加到列表中
                url_list.append(url)
            # print(title, url)

        return url_list

    def get_url_by_title_feeddd(self, title):
        """通过feeddd项目尝试获取文章URL"""

        url = None
        for item in self.soup_feeddd.find_all('item'):
            if item.title.text.startswith(title):
                url = item.link.text
                break
        return url

    def get_url_by_title_sogo(self, title):
        """通过搜狗微信搜索尝试获取文章URL"""

        payload = {'type': '2', 'query': title, 's_from': 'input', 'ie': 'utf8', '_sug_': 'n', '_sug_type_': ''}
        r = self.sess_sogo.get(self.homepage_sogo, params=payload)
        # print('get:', title, r.url)
        time.sleep(0.2+random.random()) # to avoid anti-spider
        r.encoding = 'utf-8'

        soup = BeautifulSoup(r.text, 'html.parser')
        url = None
        if not soup.find('ul', class_='news-list'):
            raise Exception('Sogo search error!')
        for news in soup.find('ul', class_='news-list'):
            if not news.name == 'li':
                continue
            if news.find('div', class_='txt-box').a.text.startswith(title):
                url = 'https://weixin.sogou.com' + news.find('div', class_='txt-box').a['href']
                break

        parsed_url = self.parse_url_sogo(url) if url else None

        return parsed_url

    def parse_url_sogo(self, url):
        """解析搜狗跳转链接，转换为真实链接
        参考文章：https://blog.csdn.net/qq_42636010/article/details/94321049
        """

        b = random.randint(0, 99)
        a = url.index('url=')
        a = url[a + 30 + b: a + 31 + b: ]
        url += '&k=' + str(b) + '&h=' + a

        r = self.sess_sogo.get(url)
        parsed_url_list = re.findall(r"url \+= '(.+)'", r.text)
        parsed_url = ''.join(parsed_url_list)
        parsed_url = re.sub(r'@', r'', parsed_url)

        if parsed_url == '':
            raise ValueError('parsed URL is empty!')

        return parsed_url


def replace_img_link(html):
    """将推文图片链接转换为外链可以访问的形式"""

    # 方法一：https://blog.csdn.net/yanjiee/article/details/52938144（失效弃用）
    # return re.sub(r'mmbiz\.qpic\.cn', 
    #               r'read.html5.qq.com/image?src=forum&q=5&r=0&imgflag=7&imageUrl=http://mmbiz.qpic.cn', 
    #               html
    #               )
    # 
    # 方法二：https://bjun.tech/blog/xphp/31
    soup = BeautifulSoup(html, 'html.parser')
    for img in soup.find_all('img'):
        img['referrerpolicy'] = 'same-origin'
    return str(soup)


def remove_break_line(html):
    """移除网页源代码中的空白行"""

    return re.sub(r'<p>(<(span|strong)>)*?(<br/?>|　| | )(<(/span|/strong)>)*?</p>',
                  r'', 
                  html
                  )


def prettify_article(html):
    """优化文章内容格式"""

    html = replace_img_link(html)
    html = remove_break_line(html)

    soup = BeautifulSoup(html, 'html.parser')
    if soup.p.img:                                          # 去除置顶的关注引导图片
        soup.p.clear()

    for child in soup.div.children:
        if child.get_text().startswith('长按或扫码') or child.get_text().startswith('欢迎点击') or child.get_text().startswith('点击'):
            p_tag = soup.new_tag('p')
            br_tag = soup.new_tag('br')
            p_tag.append(br_tag)
            child.insert_before(p_tag)
            break

        if child.name == 'p' or str(child.name).startswith('h'):
            if child.get_text():
                if not child.get_text().startswith('http'): # child为文本，包括带数字的大标题或不带数字的小标题
                    title = child.get_text()
                    if re.match(r'\d+\..*$', title):        # 如果是大标题，预先将其标签改为<h3>
                        child.name='h3'
                    else:                                   # 如果是小标题
                        if not child.name == 'p':           # 如果其标签不是<p>，则将其转化为<p>
                            child.name = 'p'
                        if str(child.previous_sibling) == '<p><br/></p>':  # 如果前面是空行（转化自上一条新闻的链接标签），将其去除
                            child.previous_sibling.clear()
                        # 如果不是空行，说明上一条目没有链接，不需要再去除
                    prev_sibling = child
                else:                                       # child为链接
                    link = child.get_text()
                    link = re.sub(r' ', r'', link)     # 去除链接末尾的 

                    if re.match(r'\d+\..*$', title):        # 判断前面的元素为大标题，为其增加超链接
                        a_tag = soup.new_tag('a', href=link)
                        a_tag.string = title
                        prev_sibling.clear()
                        prev_sibling.append(a_tag)
                    else:                                   # 判断前面元素非大标题，可能是小标题或根本没有小标题
                        a_tag = soup.new_tag('a', href=link)
                        a_tag.string = '+ ' + title
                        if title != '':                     # 有小标题，为其添加超链接
                            prev_sibling.clear()
                            prev_sibling.append(a_tag)
                        else:                               # 无小标题，将前面残余的空行（转化自上一条新闻的链接标签）转换为超链接小标题
                            # assert str(child.previous_sibling.previous_sibling) == '<p><br/></p>'
                            if str(child.previous_sibling.previous_sibling) == '<p><br/></p>':
                                child.previous_sibling.previous_sibling.clear()
                                child.previous_sibling.previous_sibling.append(a_tag)
                            # 还可能存在条目（包括大小标题及无标题）含有两个链接的情况，这里直接忽略
                            # 若含有三个链接，此处逻辑依然有误，需要注意，但目前不考虑这么复杂的情况了

                    child.clear()                       # 将原本的链接<p>标签转换为话题间的空行
                    br_tag = soup.new_tag('br')
                    child.append(br_tag)

                    title = ''                              # 经过一个链接后，将标题和标签数据清空
                    prev_sibling = None

    return str(soup)


def parse_article(url, **kwags):
    """获取文章内容，并以字典形式返回"""

    import os, sys
    sys.path.extend([os.path.dirname(os.path.dirname(os.path.abspath(__file__)))])
    import url2article
    article =  url2article.parse_article(url, **kwags)

    r = requests.get(url, **kwags)
    time.sleep(0.1)
    soup = BeautifulSoup(r.text, 'html.parser')
    title = soup.h1.text
    title = re.sub(r' |\n', '', title)
    
    article['title'] = title
    article['content'] = prettify_article(article['content'])

    return article


if __name__ == '__main__':
    get_urls = GetURLs()
    url_list = get_urls()
    
    for url in url_list:
        print(url)

    article = parse_article(url_list[0], headers=get_urls.sess_sogo.headers)
    print(article)
    print(article.keys())
