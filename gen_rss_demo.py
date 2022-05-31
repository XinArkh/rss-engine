import os
import argparse
import rss_engine


parser = argparse.ArgumentParser(description='Generate rss feed.')
parser.add_argument('-o', '--output', help='Output directory path of the rss feed.', 
                    type=str, default='./')
args = parser.parse_args()
output_dir = args.output


# --- generate zju-me rss feed ---
output = os.path.join(output_dir, 'zju-me.xml')
database = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zju-me.pkl')
logfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zju-me.log')
homepage1 = 'http://me.zju.edu.cn/meoffice/'                # 通知公告
homepage2 = 'http://me.zju.edu.cn/meoffice/6440/list.htm'   # 研究生教育
homepage3 = 'http://me.zju.edu.cn/meoffice/6469/list.htm'   # 学生工作

from user_scripts.user_script_me import fetch_src_list

url_list, title_prefix_list = fetch_src_list([homepage1, homepage2, homepage3])
rss_engine.generate_xml(url_list, title_prefix_list, 
                        rss_title='浙江大学机械工程学院通知公告', 
                        rss_link='http://me.zju.edu.cn/meoffice/', 
                        rss_description='浙江大学机械工程学院通知公告', 
                        output=output, database=database, logfile=logfile, 
                        verbose=True)


# --- generate zju-grs rss feed ---
output = os.path.join(output_dir, 'zju-grs.xml')
database = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zju-grs.pkl')
logfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zju-grs.log')
homepage = 'http://www.grs.zju.edu.cn/'

from user_scripts.user_script_grs import fetch_src_list

url_list, title_prefix_list = fetch_src_list(homepage)
rss_engine.generate_xml(url_list, title_prefix_list, 
                        rss_title='浙江大学研究生院信息公告', 
                        rss_link='http://www.grs.zju.edu.cn/', 
                        rss_description='浙江大学研究生院信息公告', 
                        output=output, database=database, logfile=logfile, 
                        verbose=True)


# --- generate jike dailypost feed ---
output = os.path.join(output_dir, 'jike-dailypost.xml')
database = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'jike-dailypost.pkl')
logfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'jike-dailypost.log')
homepage = 'https://m.okjike.com/topics/553870e8e4b0cafb0a1bef68'

from user_scripts.user_script_jike_dailypost import fetch_src_list, get_article

url_list = fetch_src_list(homepage)
rss_engine.generate_xml(url_list, parser=get_article, 
                        rss_title='一觉醒来世界发生了什么-即刻App', 
                        rss_link='https://m.okjike.com/topics/553870e8e4b0cafb0a1bef68', 
                        rss_description='一觉醒来世界发生了什么-即刻App', 
                        output=output, database=database, logfile=logfile, 
                        verbose=True)
