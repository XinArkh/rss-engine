# rss-engine: A Python framework for generating and deploying RSS feeds

A Python framework for generating and deploying RSS feeds. You can also easily and rapidly set up new RSS feeds with this framework!

In this project, the generated RSS feed is published in GitHub Page site.

## Overview

- `rss_engine.py`: core code of the framework, generating .xml file by calling its internal functions.
- `user_scripts/`: user defined scripts, assigning items to be added in RSS feed.
- `url2article.py`: parsing website contents and return relevant data. The API service provided by [URL2io](http://url2io.applinzi.com/) is utilized.
- `user_api.py`: user settings for URL2io API
- `gen_rss_demo.py`: python script to call relevant functions and generate RSS feed
- `gen_rss_demo.sh`: shell (ash) script to call `gen_rss_demo.py`

## Prerequisite

- Python(3) and the following 3rd party modules：
  - requests
  - beautifulsoup4
  - PyRSS2Gen

## Deployment

1. Sign up at URL2io and replace with valid API token in `user_api.py` 
2. Clone this repository and your GitHub Pages repository at you server (OpenWRT@RasPi in my env)
3. Configure `gen_rss_demo.sh`, set PATHs actual paths in your server
4. set executing permission of `gen_rss_demo.sh` (`chmod +x gen_rss_demo.sh`)
5. Use Linux `crontab` command to set periodical job:

```bash
crontab -e  # open editing pannel

0 8,12,18  * * *  # At minute 0 past hour 8, 12, and 18.

# exit editing pannel

crontab -l  # list tasks
service cron restart
```

## Custom Feeds

Write and put your own script in `user_scripts/` referring to the sample scripts. Then register your script in `gen_rss_demo.py`.

## Reference Links

- [Python制作RSS阅读源 | Monkey's Hut](https://monkeyhut.top/2019/06/08/Python%E5%88%B6%E4%BD%9CRSS%E9%98%85%E8%AF%BB%E6%BA%90/)
- [python生成RSS（PyRSS2Gen） - mrbean - 博客园](https://www.cnblogs.com/MrLJC/p/3732373.html)
- [crontab 定时任务——Linux Tools Quick Tutorial](https://linuxtools-rst.readthedocs.io/zh_CN/latest/tool/crontab.html)
- [Linux crontab 命令 | 菜鸟教程](https://www.runoob.com/linux/linux-comm-crontab.html)
- [Crontab.guru - The cron schedule expression editor](https://crontab.guru/)
- [cron - How to prevent from CronJob run process twice? - Ask Ubuntu](https://askubuntu.com/questions/915690/how-to-prevent-from-cronjob-run-process-twice)
- [linux shell if 参数 - image eye - 博客园](https://www.cnblogs.com/image-eye/archive/2011/08/20/2147015.html)

