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

import os, sys
sys.path.extend([os.path.dirname(os.path.dirname(os.path.abspath(__file__)))])
import url2article
import pixhost_img
import ym_verifycode


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
        self.sess_sogo.headers = {'user-agent': Faker().user_agent(), 
                                  'referer': 'https://weixin.sogou.com/weixin?type=2&s_from=input&query='
                                     '%E7%9D%A1%E5%89%8D%E6%B6%88%E6%81%AF&ie=utf8&_sug_=n&_sug_type_=',
                                  'cookie': 'SUID=0C91AE272208990A000000005C7145DC; SUV=1550927324797555; '
                                  'ssuid=8275997946; IPLOC=CN3301; SGINPUT_UPSCREEN=1656915382829; ABTEST=5|1660024272|v1; '
                                  'weixinIndexVisited=1; JSESSIONID=aaap2f8T9OAKt-B4VvWky; PHPSESSID=7k4dpsbas0a24rki02b1kg2k02; '
                                  'SNUID=2DAA941D3A3FDCF9C669D80E3B504358; ld=RZllllllll209TjGlllllpGFtwZlllllJffSVZllll9llllllZ'
                                  'lll5@@@@@@@@@@; ariaDefaultTheme=undefined'
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
        time.sleep(5+random.random()) # to avoid anti-spider
        r.encoding = 'utf-8'
        print('in get_url_by_title_sogo(): get:', title, r.url)

        soup = BeautifulSoup(r.text, 'html.parser')
        url = None
        # 若出现搜狗爬虫验证页面，尝试提交验证码通过，最多三次
        max_loop = 3
        while (not soup.find('ul', class_='news-list')) and max_loop > 0:
            max_loop -= 1

            if not soup.find('img', id='seccodeImage'): # 存在一定几率验证页面无此项，跳过直接在下个循环重新尝试
                print('重新获取页面...')
                time.sleep(5+random.random()) # to avoid anti-spider
                r = self.sess_sogo.get(self.homepage_sogo, params=payload)
                r.encoding = 'utf-8'
                soup = BeautifulSoup(r.text, 'html.parser')
                continue

            img_url = 'https://weixin.sogou.com/antispider/' + soup.find('img', id='seccodeImage')['src']
            img_bin = self.download_img_bin(img_url)
            verify_code = ym_verifycode.identify_verifycode(img_bin)

            # src_url = re.search(r'(\?|&)from=(.*?)(&antip=wx_js)?', r.url).group(1)
            src_url = re.search(r'(\?|&)from=(.+)(&antip=wx_js|$)?', r.url).group(2)
            auuid = re.search(r'var auuid = "(.*?)";', r.text).group(1)

            r = self.post_verifycode(verify_code, src_url, auuid)
            time.sleep(5+random.random()) # to avoid anti-spider
            r.encoding = 'utf-8'
            soup = BeautifulSoup(r.text, 'html.parser')
            
            if r.json()['msg'].startswith('解封成功'):
                r = self.sess_sogo.get(self.homepage_sogo, params=payload)
                time.sleep(1+random.random()) # to avoid anti-spider
                r.encoding = 'utf-8'
                soup = BeautifulSoup(r.text, 'html.parser')
                break

        if not soup.find('ul', class_='news-list'):
            # print('soup:', soup)
            raise Exception('Sogo anti-spider error!')
        for news in soup.find('ul', class_='news-list'):
            if not news.name == 'li':
                continue
            if news.find('div', class_='txt-box').a.text.startswith(title):
                url = 'https://weixin.sogou.com' + news.find('div', class_='txt-box').a['href']
                break

        # print('url:', url)
        parsed_url = self.parse_url_sogo(url) if url else None

        return parsed_url

    def download_img_bin(self, img_url):
        r = self.sess_sogo.get(img_url)
        img_bin = r.content
        
        return img_bin
        
    def post_verifycode(self, verify_code, src_url, auuid):
        post_url = 'https://weixin.sogou.com/antispider/thank.php'
        payload = {
            'c': verify_code,
            'r': src_url,
            'p': 'wx_js',
            'v': '5',
            'suuid': '',
            'auuid': auuid
        }
        r = self.sess_sogo.post(post_url, data=payload)
        print('code_status', r.text)

        return r

    def parse_url_sogo(self, url):
        """解析搜狗跳转链接，转换为真实链接
        参考文章：https://blog.csdn.net/qq_42636010/article/details/94321049
        """

        b = random.randint(0, 99)
        a = url.index('url=')
        a = url[a + 30 + b: a + 31 + b: ]
        url += '&k=' + str(b) + '&h=' + a

        r = self.sess_sogo.get(url)
        # print('parse url:', r.text)
        parsed_url_list = re.findall(r"url \+= '(.+)'", r.text)
        parsed_url = ''.join(parsed_url_list)
        parsed_url = re.sub(r'@', r'', parsed_url)

        if parsed_url == '':
            raise ValueError('parsed URL is empty!')

        return parsed_url


def replace_img_link(html, simple_method=False):
    """将推文图片链接转换为外链可以访问的形式"""

    # 方法一：https://blog.csdn.net/yanjiee/article/details/52938144（失效弃用）
    # return re.sub(r'mmbiz\.qpic\.cn', 
    #               r'read.html5.qq.com/image?src=forum&q=5&r=0&imgflag=7&imageUrl=http://mmbiz.qpic.cn', 
    #               html
    #               )
    # 
    # 方法二：https://bjun.tech/blog/xphp/31
    if simple_method:
        soup = BeautifulSoup(html, 'html.parser')
        for img in soup.find_all('img'):
            img['referrerpolicy'] = 'same-origin'

    # 方法三：将图片托管至图床
    else:
        pix = pixhost_img.PiXhost()
        sess_wx = requests.session()
        sess_wx.headers = {
            'user-agent': Faker().user_agent(),
        }
        soup = BeautifulSoup(html, 'html.parser')
        for img in soup.find_all('img'):
            src = img['src']
            img_bin = sess_wx.get(src).content
            src_new = pix.upload_img(img_bin)
            img['src'] = src_new

    return str(soup)


def remove_0xa0(html):
    """移除网页源代码中的<0xa0>"""

    return re.sub(r' ',
                  r'', 
                  html
                  )


def prettify_article(html):
    """优化文章内容格式"""

    html = replace_img_link(html, simple_method=False)
    html = remove_0xa0(html)

    soup = BeautifulSoup(html, 'html.parser')
    # if soup.p.img:                                          # 去除置顶的关注引导图片
    #     soup.p.clear()

    loop = soup.contents[0] if len(soup.contents) == 1 else soup
    for child in loop.children:
        # 跳过空标签
        if child.get_text() == '':
            continue

        # 匹配主新闻标题（1./2./3....或1、/2、/3、...）
        if re.match(r'\d+[\.、]', child.get_text()):
            child.name = 'h3'
            title_dict = {
                'title_elem': child,
                'title_type': 1,
            }

        # 匹配附加新闻标题
        elif set([c.name for c in child.descendants]) == set(['strong', 'span', None]):
            if child.name.startswith('h'):
                child.name = 'p'
            child.string = '+ ' + child.get_text()
            title_dict = {
                'title_elem': child,
                'title_type': 2,
            }

        # 匹配新闻链接
        elif child.get_text().startswith('http'):
            link = child.get_text()
            link = re.sub(r' ', r'', link)         # 去除链接末尾的 

            # 生成超链接标题
            # 若原本有标题，判断是主标题还是附加标题
            if 'title_dict' in dir() and title_dict is not None:
                if title_dict['title_type'] == 1:       # 主标题
                    title_elem = title_dict['title_elem']
                    a_tag = soup.new_tag('a', href=link)
                    a_tag.string = title_elem.get_text()
                    title_elem.clear()
                    title_elem.append(a_tag)
                
                elif title_dict['title_type'] == 2:     # 附加标题
                    title_elem = title_dict['title_elem']
                    a_tag = soup.new_tag('a', href=link)
                    a_tag.string = title_elem.get_text()
                    title_elem.clear()
                    title_elem.append(a_tag)
            
            # 若原本无标题，认为是不带标题的附加新闻
            else:
                a_tag = soup.new_tag('a', href=link)
                a_tag.string = '+'
                child.previous_sibling.insert_before(a_tag)

            # 链接转换到标题处之后，将原本的链接标签转换为空行
            child.clear()
            br_tag = soup.new_tag('br')
            child.append(br_tag)

            # 链接转换到标题处之后，归零对前一个标题元素的记录
            title_dict = None

    return str(soup)


def parse_article(url, **kwags):
    """获取文章内容，并以字典形式返回"""

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
