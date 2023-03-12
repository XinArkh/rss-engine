# RSSEngine: A lightweight RSS feed generator

RSSEngine is a lightweight and extensible RSS feed generator, implemented by Python language. 

With RSSEngine, you can easily and rapidly generate RSS feed for arbitrary websites, with your custom scripts.

RSSEngine is powered by [PyRSS2Gen](http://www.dalkescientific.com/Python/PyRSS2Gen.html).

## Feed List

### Maintaining

- 睡前消息-马前卒工作室: [https://www.xinwu.me/rss/bedtime-story.xml](https://www.xinwu.me/rss/bedtime-story.xml)
- 即刻App-一觉醒来世界发生了什么: [https://www.xinwu.me/rss/jike-dailypost.xml](https://www.xinwu.me/rss/jike-dailypost.xml)
- 少数派-全文版: [https://www.xinwu.me/rss/sspai.xml](https://www.xinwu.me/rss/sspai.xml)
- 王孟源的博客: [https://www.xinwu.me/rss/wmyblog.xml](https://www.xinwu.me/rss/wmyblog.xml)
- 浙江大学医学院通知: [xinwu.me/rss/zju-cmm.xml](xinwu.me/rss/zju-cmm.xml)
- 浙江大学研究生院通知: [xinwu.me/rss/zju-grs.xml](xinwu.me/rss/zju-grs.xml)
- 浙江大学机械工程学院通知: [https://www.xinwu.me/rss/zju-me.xml](https://www.xinwu.me/rss/zju-me.xml)

### Archived

- 浙江大学疫情防控工作通知: [https://www.xinwu.me/rss/zju-yqfk.xml](https://www.xinwu.me/rss/zju-yqfk.xml)

## Prerequisite

- Python(3) and the following 3rd party modules：
  - requests
  - beautifulsoup4
  - PyRSS2Gen
  
  Custom user scripts may induce extra modules as well.

## Deployment

The following procedure shows how to deploy RSSEngine in a Linux server. 

1. Clone this repository and your target website (GitHub Pages for my example) repository in you own server (OpenWRT@RasPi in my case)
2. Fill in your API tokens in `user_api.py` (optional when relevant functions are required)
3. Edit `run_script.sh`, set relevant paths in your server
4. Add executing permission for `run_script.sh` (i.e. `chmod +x run_script.sh`)
5. Use Linux `crontab` command to set a periodical job:

```bash
## open editing pannel
>>> crontab -e
# tip: you can refer to https://crontab.guru/ to check your crontab commands
# redirect output messages to logfile.
>>> 0/30 * * * * /PATH/TO/run_script.sh >> /PATH/TO/rss.log
# exit the editing pannel (:wq)

## optional: list current jobs and refresh cron service
>>> crontab -l
>>> service cron restart
```

## Custom Feeds

Write and put your own script in `user_scripts/` and register it in `run_script.py`. It's pretty easy, you can refer to existing sample scripts.


## By Me a Coffee

If you like this project and want to show your support, you can buy me a coffee!

![donate](./donate.png)