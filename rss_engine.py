import time
import datetime
import pickle
import PyRSS2Gen

import url2article


def is_new_article(url, url_set):
    '''
    判断url是否已存在于url_set中，从而判断是否为新文章
    '''
    if url in url_set:
        return False
    else:
        return True


def is_article_up_to_date(article_pubdate, within_days=365):
    '''
    判断文章发布日期是否太久远
    '''
    if datetime.datetime.now() - article_pubdate <= datetime.timedelta(days=within_days):
        return True
    else:
        return False


def log(msg: str, path: str):
    '''
    写入日志文件
    '''
    if msg != '':
        with open(path, 'a') as f:
            f.writelines(msg)


def generate_xml(url_list, title_prefix_list=None, parser=None, headers=None, 
                 rss_title='rss engine demo', 
                 rss_description='rss engine demo', 
                 rss_link='https://github.com/XinArkh/rss-engine', 
                 within_days=365, max_item=50, 
                 output='./demo.xml', database='./demo.pkl', logfile='./demo.log', 
                 verbose=False
                ):
    '''生成rss xml文件

    url_list: 要生成的文章链接列表，每一个链接对应一个文章
    title_prefix_list: 文章标题前缀，和输入的链接一一对应，可选
    parser: 文章解析器，从一个文章链接中解析得到其信息，包括链接、日期、内容、标题，默认使用内置的URL2io解析器
    headers: 解析器请求网页时可能用到的请求头
    rss_title: RSS推送标题
    rss_description: RSS推送描述
    rss_link: RSS推送链接
    output: xml文件输出路径
    database: 缓存数据库路径
    logfile: 日志文件路径
    within_days: 限定日期，过于久远的文章不再收录
    max_item: 最大保留文章数目
    verbose: 是否输出详细日志，默认否
    '''

    if not title_prefix_list: title_prefix_list = [''] * len(url_list)
    assert len(url_list) == len(title_prefix_list)
    if not parser: parser = url2article.get_article

    try:                        # 尝试打开本地数据库，数据库中保存url记录和rss items
        with open(database, 'rb') as f:
            url_set, item_list = pickle.load(f)
    except FileNotFoundError:   # 本地无现有数据库，则新建对应数据
        url_set = set()
        item_list = []

    log_str = ''
    item_num = 0
    for url, title_prefix in zip(url_list, title_prefix_list):
        if is_new_article(url, url_set):
            try:
                article = parser(url, headers)
                article_link = article['url']
                article_title = title_prefix + article['title']
                article_pubdate = datetime.datetime.strptime(article['date'], '%Y-%m-%d %H:%M:%S')
                article_description = article['content']
                if is_article_up_to_date(article_pubdate, within_days=within_days):
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
        item_list.sort(key=lambda rss_item: rss_item.pubDate, reverse=True) # 按照发表时间降序排序
        if len(item_list) > max_item: item_list = item_list[:max_item]      # 控制条目数量
        
        # 生成xml文件
        rss = PyRSS2Gen.RSS2(title=rss_title, 
                             link=rss_link, 
                             description=rss_description, 
                             lastBuildDate=datetime.datetime.now(), 
                             items=item_list)
        rss.write_xml(open(output, 'w', encoding='utf-8'), encoding='utf-8')
        if verbose: print('%s: rss file updated.' %rss_title)

        # 写入本地数据库
        with open(database, 'wb') as f:
            pickle.dump([url_set, item_list], f)
        if verbose: print('%s: database updated.' %rss_title)

    # 写入日志文件
    log_str += '------ %s: %d new rss items updated ------\n\n' % (datetime.datetime.now(), item_num)
    log(log_str, logfile)
    if verbose: print('%s: log file updated.' %rss_title)


if __name__ == '__main__':
    # example
    from user_scripts.user_script_grs import fetch_src_list
    url_list, title_prefix_list = fetch_src_list('http://www.grs.zju.edu.cn/')

    generate_xml(url_list, title_prefix_list, verbose=True)
