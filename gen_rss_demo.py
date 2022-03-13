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
database = 'zju-me.pkl'
logfile = 'zju-me.log'
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
database = 'zju-grs.pkl'
logfile = 'zju-grs.log'
homepage = 'http://www.grs.zju.edu.cn/'

from user_scripts.user_script_grs import fetch_src_list

url_list, title_prefix_list = fetch_src_list(homepage)
rss_engine.generate_xml(url_list, title_prefix_list, 
                        rss_title='浙江大学研究生院信息公告', 
                        rss_link='http://www.grs.zju.edu.cn/', 
                        rss_description='浙江大学研究生院信息公告', 
                        output=output, database=database, logfile=logfile, 
                        verbose=True)
