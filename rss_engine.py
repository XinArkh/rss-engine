import time
import datetime
import pickle
import PyRSS2Gen

import url2article


class RSSEngine:
    """RSSEngine, generate RSS feed for arbitrary source!"""

    def __init__(self, 
                 # rss channel elements
                 rss_title='demo', 
                 rss_link='https://github.com/XinArkh/rss-engine', 
                 rss_description='demo', 
                 rss_language=None,
                 rss_copyright=None,
                 rss_managingEditor=None,
                 rss_webMaster=None,
                 rss_pubDate=None,
                 rss_lastBuildDate=None,
                 rss_category=None,
                 rss_generator='RSSEngine powered by PyRSS2Gen-1.1.0',
                 rss_docs=None,
                 rss_cloud=None,
                 rss_ttl=None,
                 rss_icon=None, # for channel element 'image'
                 rss_rating=None,
                 rss_textInput=None,
                 rss_skipHours=None,
                 rss_skipDays=None,
                 # custom parameters
                 timezone=+8,
                 within_days=365, 
                 max_item_num=10, 
                 output='./demo.xml', 
                 database='./demo.pkl', 
                 logfile='./demo.log', 
                 double_check=False,
                 verbose=False
                 ):

        self.rss_channel_elem = {}
        self.rss_channel_elem['title'] = rss_title
        self.rss_channel_elem['link'] = rss_link
        self.rss_channel_elem['description'] = rss_description
        self.rss_channel_elem['language'] = rss_language
        self.rss_channel_elem['copyright'] = rss_copyright
        self.rss_channel_elem['managingEditor'] = rss_managingEditor
        self.rss_channel_elem['webMaster'] = rss_webMaster
        self.rss_channel_elem['pubDate'] = rss_pubDate
        self.rss_channel_elem['lastBuildDate'] = rss_lastBuildDate
        self.rss_channel_elem['categories'] = rss_category
        self.rss_channel_elem['generator'] = rss_generator
        self.rss_channel_elem['docs'] = rss_docs
        self.rss_channel_elem['cloud'] = rss_cloud
        self.rss_channel_elem['ttl'] = rss_ttl
        self.rss_channel_elem['image'] = PyRSS2Gen.Image(url=rss_icon, 
                                                         title='icon', 
                                                         link=rss_icon) if rss_icon else None
        self.rss_channel_elem['rating'] = rss_rating
        self.rss_channel_elem['textInput'] = rss_textInput
        self.rss_channel_elem['skipHours'] = rss_skipHours
        self.rss_channel_elem['skipDays'] = rss_skipDays

        self.timezone = datetime.timezone(datetime.timedelta(hours=timezone))
        self.within_days = within_days
        self.max_item_num = max_item_num
        self.output = output
        self.database = database
        self.logfile = logfile
        self.double_check = double_check
        self.verbose = verbose

        self.article_parser = url2article.parse_article
        self.article_parser_params = None

    def is_url_already_collected(self, url, url_set):
        """Whether the URL already collected in the database"""

        if url in url_set:
            return True
        else:
            return False

    def is_title_already_collected(self, title, title_list):
        """Whether the title already collected in the database"""

        if title in title_list:
            return True
        else:
            return False

    def local_time(self):
        """Get current time for the given timezone"""
        
        utc_time = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
        return utc_time.astimezone(self.timezone)

    def is_article_up_to_date(self, article_pubdate):
        """Whether the article is up to date"""

        if self.local_time() - article_pubdate <= datetime.timedelta(days=self.within_days):
            return True
        else:
            return False
        
    def log(self, msg: str, path: str):
        """Record log file"""

        if msg != '':
            with open(path, 'a', encoding='utf-8') as f:
                f.writelines(msg)

    def write_database(self, url_set, item_list):
        """Write URL set and item list to local database"""

        with open(self.database, 'wb') as f:
            pickle.dump([url_set, item_list], f)
        if self.verbose: print('%s: database updated.' % self.rss_channel_elem['title'])

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
            if not self.is_url_already_collected(url, url_set):
                # try parsing url
                try:
                    if self.article_parser_params:
                        article = self.article_parser(url, **self.article_parser_params)
                    else:
                        article = self.article_parser(url)
                except Exception as e:
                    log_str += 'item parsing failed: ' + title_prefix + url + ' : ' + str(e) + '\n'
                    if self.verbose: print('item parsing failed:', title_prefix, url, ':', str(e))
                    continue

                # try add article
                try:
                    article_item = {}
                    if 'title' in article.keys():
                        article_item['title'] = title_prefix + article['title']
                    if 'url' in article.keys():
                        article_item['link'] = article['url']
                        article_item['guid'] = article['url']
                    if 'content' in article.keys():
                        article_item['description'] = article['content']
                    if 'author' in article.keys():
                        article_item['author'] = article['author']
                    if 'categories' in article.keys():
                        article_item['categories'] = article['categories']
                    if 'comments' in article.keys():
                        article_item['comments'] = article['comments']
                    if 'enclosure' in article.keys():
                        article_item['enclosure'] = article['enclosure']
                    if 'date' in article.keys():
                        article_pubdate = datetime.datetime.strptime(str(article['date']), 
                                                                     '%Y-%m-%d %H:%M:%S').replace(tzinfo=self.timezone)
                        # pubdate format in PyRSS2Gen must be in GMT
                        article_item['pubDate'] = article_pubdate.astimezone(datetime.timezone.utc)
                    if 'source' in article.keys():
                        article_item['source'] = article['source']

                    assert 'title' in article_item.keys() or 'description' in article_item.keys()

                    article_item_simp = article_item.copy()
                    article_item_simp.pop('description', None)

                    if self.double_check:
                        if self.is_title_already_collected(article_item['title'], [item.title for item in item_list]):
                            continue

                    if self.is_article_up_to_date(article_pubdate):
                        item_list.append(PyRSS2Gen.RSSItem(**article_item))

                        log_str += 'item added: ' + str(article_item_simp) + '\n'
                        if self.verbose: print('item added:', article_item_simp)
                        item_num += 1
                    
                    else:
                        log_str += 'item out of date, skipped: ' + str(article_item_simp) + '\n'
                        if self.verbose: print('item out of date, skipped:', article_item_simp)
                    
                    url_set.add(url)

                except Exception as e:
                    article_simp = article.copy()
                    article_simp.pop('content', None)

                    log_str += 'item add failed: ' + str(article_simp) + ' : ' + str(e) + '\n'
                    if self.verbose: print('item add failed:', article_simp, ':', str(e))

                time.sleep(0.01) # avoid anti-spider

        if item_num > 0:
            item_list.sort(key=lambda rss_item: rss_item.pubDate, reverse=True) # descending sorting
            if len(item_list) > self.max_item_num:                              # limit item amount
                item_list = item_list[:self.max_item_num]

            # generate rss xml file
            self.rss_channel_elem['items'] = item_list
            self.rss_channel_elem['lastBuildDate'] = datetime.datetime.utcnow()
            rss = PyRSS2Gen.RSS2(**self.rss_channel_elem)
            
            rss.write_xml(open(self.output, 'w', encoding='utf-8'), encoding='utf-8')
            if self.verbose: print('%s: rss file updated, %d rss items updated.' % (self.rss_channel_elem['title'], item_num))
            self.write_database(url_set, item_list)

        log_str += '------ %s: %d new rss items updated ------\n\n' % (datetime.datetime.now(), item_num)
        self.log(log_str, self.logfile)
        if self.verbose: print('%s: log file updated.' % self.rss_channel_elem['title'])


if __name__ == '__main__':
    # example
    from user_scripts.user_script_jike_dailypost import gen_url_list, parse_article
    url_list = gen_url_list('https://m.okjike.com/topics/553870e8e4b0cafb0a1bef68')
    rss = RSSEngine(verbose=True)
    rss.set_article_parser(parse_article)
    rss.generate_xml(url_list)
