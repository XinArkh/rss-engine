# RSSEngine: A lightweight RSS feed generator

RSSEngine is a lightweight and extensible RSS feed generator, implemented by Python language. 

With RSSEngine, you can easily and rapidly generate RSS feed for arbitrary websites, with your custom scripts.

RSSEngine is powered by [PyRSS2Gen](http://www.dalkescientific.com/Python/PyRSS2Gen.html).

## Existing Feeds

- 睡前消息-马前卒工作室: [https://www.xinwu.me/rss/bedtime-story.xml](https://www.xinwu.me/rss/bedtime-story.xml)
- 即刻App-一觉醒来世界发生了什么: [https://www.xinwu.me/rss/jike-dailypost.xml](https://www.xinwu.me/rss/jike-dailypost.xml)
- 少数派-全文版: [https://www.xinwu.me/rss/sspai.xml](https://www.xinwu.me/rss/sspai.xml)
- 浙江大学医学院通知: [xinwu.me/rss/zju-cmm.xml](xinwu.me/rss/zju-cmm.xml)
- 浙江大学研究生院通知: [xinwu.me/rss/zju-grs.xml](xinwu.me/rss/zju-grs.xml)
- 浙江大学机械工程学院通知: [https://www.xinwu.me/rss/zju-me.xml](https://www.xinwu.me/rss/zju-me.xml)

## Prerequisite

- Python(3) and the following 3rd party modules：
  - requests
  - beautifulsoup4
  - PyRSS2Gen
  
  Custom user scripts may induce extra modules as well.

## Deployment

The following procedure shows how to deploy RSSEngine in a Linux server. 

1. Clone this repository and your target website (GitHub Pages for my example) repository in you own server (OpenWRT@RasPi in my case)
2. Fill in your API tokens in `user_api.py` (optional if you need relevant functions)
3. Edit `run_script.sh`, set relevant paths in your server
4. Add executing permission for `run_script.sh` (i.e. `chmod +x gen_rss_demo.sh`)
5. Use Linux `crontab` command to set a periodical job:

```bash
## open editing pannel
crontab -e
# tip: you can refer to https://crontab.guru/ to check your crontab commands
# redirect output messages to logfile.
>>> 0/30 * * * * /PATH/TO/run_script.sh >> /PATH/TO/rss.log
# exit the editing pannel (:wq)

## optional: list current jobs and refresh cron service
crontab -l
service cron restart
```

## Custom Feeds

Write and put your own script in `user_scripts/` and register it in `run_script.py`. It's pretty easy, you can refer to existing sample scripts.

## Reference Links

- [Python制作RSS阅读源 | Monkey's Hut](https://monkeyhut.top/2019/06/08/Python%E5%88%B6%E4%BD%9CRSS%E9%98%85%E8%AF%BB%E6%BA%90/)
- [python生成RSS（PyRSS2Gen） - mrbean - 博客园](https://www.cnblogs.com/MrLJC/p/3732373.html)
- [crontab 定时任务——Linux Tools Quick Tutorial](https://linuxtools-rst.readthedocs.io/zh_CN/latest/tool/crontab.html)
- [Linux crontab 命令 | 菜鸟教程](https://www.runoob.com/linux/linux-comm-crontab.html)
- [Crontab.guru - The cron schedule expression editor](https://crontab.guru/)
- [cron - How to prevent from CronJob run process twice? - Ask Ubuntu](https://askubuntu.com/questions/915690/how-to-prevent-from-cronjob-run-process-twice)
- [linux shell if 参数 - image eye - 博客园](https://www.cnblogs.com/image-eye/archive/2011/08/20/2147015.html)
