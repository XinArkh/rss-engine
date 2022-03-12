import os
import time
import datetime
import pickle
import requests
import PyRSS2Gen

import url2article
import get_url_list


def get_url_content(url):
    '''
    获取网页源码，以字符串方式返回
    '''
    r = requests.get(url)
    r.raise_for_status()
    r.encoding = 'utf-8'
    # print(r.text)
    return r.text


def is_new_article(url, url_set):
    '''
    判断url是否已存在于url_set中，从而判断是否为新文章
    '''
    if url in url_set:
        return False
    else:
        return True


def is_article_up_to_date(article_pubdate, days=365):
    '''
    判断文章发布日期是否太久远
    '''
    if datetime.datetime.now() - article_pubdate <= datetime.timedelta(days=days):
        return True
    else:
        return False


def log(msg: str, path):
    '''
    写入日志文件
    '''
    if msg != '':
        with open(path, 'a') as f:
            f.writelines(msg)


def generate_xml(verbose=False):
    '''
    生成rss xml文件
    '''
    try:                        # 尝试打开本地数据库，数据库中保存url记录和rss items
        with open(data_storage, 'rb') as f:
            url_set, item_list = pickle.load(f)
    except FileNotFoundError:   # 本地无现有数据库，则新建对应数据
        url_set = set()
        item_list = []

    url_list1 = get_url_list.get_url_list_tzgg(homepage1)
    url_list2 = get_url_list.get_url_list_yjsjy(homepage2)
    url_list3 = get_url_list.get_url_list_xsgz(homepage3)

    log_str = ''
    item_num = 0
    for url_list, title_prefix in zip([url_list1, url_list2, url_list3], ['【通知公告】', '【研究生教育】', '【学生工作】']):
        for url in url_list:
            if is_new_article(url, url_set):
                try:
                    article = url2article.get_article(url)
                    article_link = article['url']
                    article_title = title_prefix + article['title']
                    article_pubdate = datetime.datetime.strptime(article['date'], '%Y-%m-%d %H:%M:%S')
                    article_description = article['content']

                    if is_article_up_to_date(article_pubdate):
                        item_list.append(PyRSS2Gen.RSSItem(title=article_title, 
                                                           link=article_link, 
                                                           description=article_description, 
                                                           guid=article_link, 
                                                           pubDate=article_pubdate))
                        log_str += 'item added: ' + article_title +' ' + str(article['date']) +' ' + article_link + '\n'
                        if verbose: print('item added:', article_title, article['date'], article_link)
                        item_num += 1
                        url_set.add(url)
                    else:
                        log_str += 'item out of date, skipped: ' + article_title +' ' + str(article['date']) +' ' + article_link + '\n'
                        if verbose: print('item out of date, skipped:', article_title, article['date'], article_link)
                except:
                    log_str += 'item add failed: ' + article_title +' ' + str(article['date']) +' ' + article_link + '\n'
                    if verbose: print('item add failed:', article_title, article['date'], article_link)

            time.sleep(0.1) # 防止访问太快被屏蔽

    if item_num > 0:
        # 生成xml文件
        item_list.sort(key=lambda rss_item: rss_item.pubDate, reverse=True) # 按照发表时间降序排序
        rss = PyRSS2Gen.RSS2(title='浙江大学机械工程学院通知公告', 
                             link='http://me.zju.edu.cn/meoffice/', 
                             description='浙江大学机械工程学院通知公告', 
                             lastBuildDate=datetime.datetime.now(), 
                             items=item_list)
        rss.write_xml(open(xml_path, 'w', encoding='utf-8'), encoding='utf-8')
        if verbose: print('rss file updated.')

        # 写入本地数据库
        with open(data_storage, 'wb') as f:
            pickle.dump([url_set, item_list], f)
        if verbose: print('database updated.')

    # 写入日志文件
    log_str += '------ %s: %d new rss items updated ------\n\n' % (datetime.datetime.now(), item_num)
    log(log_str, log_path)
    if verbose: print('log file updated.')



if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate zju me rss feed.')
    parser.add_argument('-o', '--output', help='the output path of the xml file',
                        type=str, default=os.path.dirname(os.path.abspath(__file__)))
    parser.add_argument('-d', '--database', help='The data storage path.', 
                        type=str, default=os.path.dirname(os.path.abspath(__file__)))
    parser.add_argument('-l', '--log', help='The log file path.', 
                        type=str, default=os.path.dirname(os.path.abspath(__file__)))
    args = parser.parse_args()

    xml_path = os.path.join(args.output, 'zju-me.xml')
    data_storage = os.path.join(args.database, 'data_storage.pkl')
    log_path = os.path.join(args.log, 'logfile.txt')
    
    homepage1 = 'http://me.zju.edu.cn/meoffice/'                # 通知公告
    homepage2 = 'http://me.zju.edu.cn/meoffice/6440/list.htm'   # 研究生教育
    homepage3 = 'http://me.zju.edu.cn/meoffice/6469/list.htm'   # 学生工作

    generate_xml(verbose=True)
