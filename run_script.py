import os
import argparse
import rss_engine


if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')):
    os.mkdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output'))
parser = argparse.ArgumentParser(description='Generate rss feed.')
parser.add_argument('-o', '--output', 
                    help='Output directory path of the rss feed.', 
                    type=str, 
                    default=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output'))
args = parser.parse_args()
output_dir = args.output


## -------------------------------------------------- ##
# --- generate sspai rss feed --- #
file_name = 'sspai'
output = os.path.join(output_dir, file_name+'.xml')
database = os.path.join(output_dir, file_name+'.pkl')
logfile = os.path.join(output_dir, file_name+'.log')
homepage = 'https://sspai.com/feed'

from user_scripts.user_script_sspai import gen_url_list, parse_article

url_list = gen_url_list(homepage)
rss = rss_engine.RSSEngine(rss_title='少数派', 
                           rss_link='https://sspai.com', 
                           rss_description='少数派RSS Feed-文章完整抓取版', 
                           rss_language='zh-CN',
                           rss_managingEditor='contact@sspai.com (少数派)',
                           rss_icon='https://t75.pixhost.to/thumbs/126/299184373_ouezg12u_400x400.png',
                           output=output, database=database, logfile=logfile, 
                           verbose=True)
rss.set_article_parser(parse_article, homepage=homepage)
rss.generate_xml(url_list)


# --- generate zju-me rss feed --- #
file_name = 'zju-me'
output = os.path.join(output_dir, file_name+'.xml')
database = os.path.join(output_dir, file_name+'.pkl')
logfile = os.path.join(output_dir, file_name+'.log')
homepage1 = 'http://me.zju.edu.cn/meoffice/'                # 通知公告
homepage2 = 'http://me.zju.edu.cn/meoffice/6440/list.htm'   # 研究生教育
homepage3 = 'http://me.zju.edu.cn/meoffice/6469/list.htm'   # 学生工作

from user_scripts.user_script_zju_me import gen_url_list, parse_article

url_list, title_prefix_list = gen_url_list([homepage1, homepage2, homepage3])
rss = rss_engine.RSSEngine(rss_title='浙江大学机械工程学院通知公告', 
                           rss_link='http://me.zju.edu.cn/meoffice/', 
                           rss_description='浙江大学机械工程学院通知公告', 
                           output=output, database=database, logfile=logfile, 
                           verbose=True)
rss.set_article_parser(parse_article)
rss.generate_xml(url_list, title_prefix_list)


# --- generate zju-grs rss feed --- #
file_name = 'zju-grs'
output = os.path.join(output_dir, file_name+'.xml')
database = os.path.join(output_dir, file_name+'.pkl')
logfile = os.path.join(output_dir, file_name+'.log')
homepage = 'http://www.grs.zju.edu.cn/'

from user_scripts.user_script_zju_grs import gen_url_list, parse_article

url_list, title_prefix_list = gen_url_list(homepage)
rss = rss_engine.RSSEngine(rss_title='浙江大学研究生院信息公告', 
                           rss_link=homepage, 
                           rss_description='浙江大学研究生院信息公告', 
                           output=output, database=database, logfile=logfile, 
                           verbose=True)
rss.set_article_parser(parse_article)
rss.generate_xml(url_list, title_prefix_list)


# --- generate zju-cmm rss feed --- #
file_name = 'zju-cmm'
output = os.path.join(output_dir, file_name+'.xml')
database = os.path.join(output_dir, file_name+'.pkl')
logfile = os.path.join(output_dir, file_name+'.log')
homepage1 = 'http://www.cmm.zju.edu.cn/yltx/list.htm'   # 医路同行
homepage2 = 'http://www.cmm.zju.edu.cn/38700/list.htm'  # 研究生教育

from user_scripts.user_script_zju_cmm import gen_url_list, parse_article

url_list, title_prefix_list = gen_url_list([homepage1, homepage2])
rss = rss_engine.RSSEngine(rss_title='浙江大学医学院信息公告', 
                           rss_link=homepage, 
                           rss_description='浙江大学医学院信息公告', 
                           within_days=365*15,
                           output=output, database=database, logfile=logfile, 
                           verbose=True)
rss.set_article_parser(parse_article)
rss.generate_xml(url_list, title_prefix_list)


# --- generate jike dailypost feed --- #
file_name = 'jike-dailypost'
output = os.path.join(output_dir, file_name+'.xml')
database = os.path.join(output_dir, file_name+'.pkl')
logfile = os.path.join(output_dir, file_name+'.log')
homepage = 'https://m.okjike.com/topics/553870e8e4b0cafb0a1bef68'

from user_scripts.user_script_jike_dailypost import gen_url_list, parse_article

url_list = gen_url_list(homepage)
rss = rss_engine.RSSEngine(rss_title='一觉醒来世界发生了什么-即刻App', 
                           rss_link=homepage, 
                           rss_description='一觉醒来世界发生了什么-即刻App', 
                           rss_icon='https://t75.pixhost.to/thumbs/127/299240346_300x300a0a0.jpg',
                           max_item_num=12, 
                           output=output, database=database, logfile=logfile, 
                           verbose=True)
rss.set_article_parser(parse_article)
rss.generate_xml(url_list)


# --- generate 睡前消息 feed --- #
file_name = 'bedtime-story'
output = os.path.join(output_dir, file_name+'.xml')
database = os.path.join(output_dir, file_name+'.pkl')
logfile = os.path.join(output_dir, file_name+'.log')

from user_scripts.user_script_bedtime_story import GetURLs, parse_article

get_urls = GetURLs()
url_list = get_urls()
rss = rss_engine.RSSEngine(rss_title='睡前消息', 
                           rss_link='https://www.xinwu.me/rss/bedtime-story.xml', 
                           rss_description='睡前消息-马前卒工作室', 
                           rss_icon='https://t75.pixhost.to/thumbs/127/299239783_v2-d6e9e8af50b94f57f1baf8faaf0ed884_xl.jpg',
                           output=output, database=database, logfile=logfile, 
                           double_check=True, 
                           verbose=True)
rss.set_article_parser(parse_article, headers=get_urls.sess_sogo.headers)
rss.generate_xml(url_list)
