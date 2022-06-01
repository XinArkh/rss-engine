import time
import datetime
import pickle
import PyRSS2Gen

import url2article


class RSSEngine:
    """RSSEngine, generate RSS feed for arbitrary source!"""

    def __init__(self, rss_title='demo', rss_description='demo', 
                 rss_link='https://github.com/XinArkh/rss-engine', 
                 within_days=365, max_item_num=50, 
                 output='./demo.xml', database='./demo.pkl', logfile='./demo.log', 
                 verbose=False):
        self.rss_title = rss_title
        self.rss_description = rss_description
        self.rss_link = rss_link
        self.within_days = within_days
        self.max_item_num = max_item_num
        self.output = output
        self.database = database
        self.logfile = logfile
        self.verbose = verbose

        self.article_parser = url2article.parse_article
        self.article_parser_params = None

    def is_already_added(self, url, url_set):
        """Whether the URL already added in the collection"""

        if url in url_set:
            return True
        else:
            return False

    def is_article_up_to_date(self, article_pubdate):
        """Whether the article is up to date"""

        if datetime.datetime.now() - article_pubdate <= datetime.timedelta(days=self.within_days):
            return True
        else:
            return False
        
    def log(self, msg: str, path: str):
        """record log file"""

        if msg != '':
            with open(path, 'a') as f:
                f.writelines(msg)

    def write_database(self, url_set, item_list):
        """Write URL set and item list to local database"""

        with open(self.database, 'wb') as f:
            pickle.dump([url_set, item_list], f)
        if self.verbose: print('%s: database updated.' %self.rss_title)

    def set_article_parser(self, parser_func, **kwargs):
        """Set custom article parser"""

        self.article_parser = parser_func
        self.article_parser_params = kwargs

    def generate_xml(self, url_list, title_prefix_list=None):
        """Generate RSS xml file"""

        if not title_prefix_list: title_prefix_list = [''] * len(url_list)
        assert len(url_list) == len(title_prefix_list)

        try:                        # try opening local database, in which url and rss items are saved
            with open(self.database, 'rb') as f:
                url_set, item_list = pickle.load(f)
        except FileNotFoundError:   # if no local database is found, create a new one
            url_set = set()
            item_list = []

        log_str = ''
        item_num = 0
        for url, title_prefix in zip(url_list, title_prefix_list):
            if not self.is_already_added(url, url_set):
                try:
                    if self.article_parser_params:
                        article = self.article_parser(url, **self.article_parser_params)
                    else:
                        article = self.article_parser(url)

                    article_link = article['url']
                    article_title = title_prefix + article['title']
                    article_pubdate = datetime.datetime.strptime(article['date'], '%Y-%m-%d %H:%M:%S')
                    article_description = article['content']

                    if self.is_article_up_to_date(article_pubdate):
                        item_list.append(PyRSS2Gen.RSSItem(title=article_title, 
                                                           link=article_link, 
                                                           description=article_description, 
                                                           guid=article_link, 
                                                           pubDate=article_pubdate))
                        log_str += 'item added: ' + article_title +' ' + str(article['date']) +' ' + article_link + '\n'
                        if self.verbose: print('item added:', article_title, article['date'], article_link)
                        item_num += 1
                        url_set.add(url)
                    else:
                        log_str += 'item out of date, skipped: ' + article_title +' ' + str(article['date']) +' ' + article_link + '\n'
                        if self.verbose: print('item out of date, skipped:', article_title, article['date'], article_link)
                except:
                    log_str += 'item add failed: ' + article_title +' ' + str(article['date']) +' ' + article_link + '\n'
                    if self.verbose: print('item add failed:', article_title, article['date'], article_link)

            time.sleep(0.01) # avoid network blockdown

        if item_num > 0:
            item_list.sort(key=lambda rss_item: rss_item.pubDate, reverse=True) # descending sorting
            if len(item_list) > self.max_item_num:                              # control item amount
                item_list = item_list[:self.max_item_num]

            # generate rss xml file
            rss = PyRSS2Gen.RSS2(title=self.rss_title, 
                                 link=self.rss_link, 
                                 description=self.rss_description, 
                                 lastBuildDate=datetime.datetime.now(), 
                                 items=item_list)
            
            rss.write_xml(open(self.output, 'w', encoding='utf-8'), encoding='utf-8')
            if self.verbose: print('%s: rss file updated.' %self.rss_title)
            self.write_database(url_set, item_list)

        log_str += '------ %s: %d new rss items updated ------\n\n' % (datetime.datetime.now(), item_num)
        self.log(log_str, self.logfile)
        if self.verbose: print('%s: log file updated.' %self.rss_title)


if __name__ == '__main__':
    # example
    from user_scripts.user_script_grs import gen_url_list
    url_list, title_prefix_list = gen_url_list('http://www.grs.zju.edu.cn/')
    # generate_xml(url_list, title_prefix_list, verbose=True)
    rss = RSSEngine(verbose=True)
    rss.generate_xml(url_list, title_prefix_list)