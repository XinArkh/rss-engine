# zju-me-rss: An RSS feed generator for ME, ZJU

本项目用于定时生成并发布[浙江大学机械工程学院](http://me.zju.edu.cn/meoffice/)的新闻公告 RSS 源。生成的 RSS 源发布在 GitHub Pages 的子页面，可以通过一般的 RSS 阅读器订阅。

与另一个项目 [zju-grs-rss](https://github.com/XinArkh/zju-grs-rss) 相同，本项目的建立基于自制的 `rss_engine` 基础框架。在此框架下，可以通过简单的编辑实现自定义 RSS 源的快速搭建。

## Overview

- `rss_engine.py`: RSS 框架主体部分，通过调用该程序来生成 .xml 文件
- `get_url_list.py`: 实现了自定义网页抓取区域的函数，更改抓取内容主要修改这一文件
- `url2article.py`: 解析网页内容，返回相关信息，主要调用了 `URL2io` 提供的网页解析 API 服务
- `data_storage.pkl`: 存储 RSS 生成的历史数据
- `logfile.txt`: 日志文件
- `xxx.xml`: 生成的 .xml 文件示例
- `update_rss_feed.sh`: 生成并发布 RSS Feed 的服务器端脚本（以树莓派 OpenWRT 系统为例）

## Prerequisite

- Python(3) 及以下第三方库：
  - requests
  - beautifulsoup4
  - PyRSS2Gen

## Deployment

1. **注册并替换** `url2article.py` **的用户 token**
2. 在自己的服务器克隆本仓库以及自己的 GitHub Pages 对应仓库
3. 配置 `update_rss_feed.sh` 脚本，将其中的各项路径修改为实际的存放路径
4. 为 `update_rss_feed.sh` 添加执行权限（`chmod +x update_rss_feed.sh`）
5. 使用 Linux crontab 命令，设置脚本定时运行：

```bash
crontab -e  # 进入编辑

* */23 * * * /root/update_rss_feed.sh  # 每隔23小时运行一次（保险起见不使用边界值24，未作深究）
# 退出编辑

crontab -l  # 查看定时任务列表
service cron restart
```

## 自定义

主要通过修改 `get_url_list.py` 中的 `get_url_list*()` 函数来自定义需要抓取的页面区域。根据函数修改的具体情况，在 `rss_engine.py` 调用该函数的对应部分也需要进行基本的配置。

## Reference Links

- [Python制作RSS阅读源 | Monkey's Hut](https://monkeyhut.top/2019/06/08/Python%E5%88%B6%E4%BD%9CRSS%E9%98%85%E8%AF%BB%E6%BA%90/)
- [python生成RSS（PyRSS2Gen） - mrbean - 博客园](https://www.cnblogs.com/MrLJC/p/3732373.html)
- [crontab 定时任务——Linux Tools Quick Tutorial](https://linuxtools-rst.readthedocs.io/zh_CN/latest/tool/crontab.html)
- [Linux crontab 命令 | 菜鸟教程](https://www.runoob.com/linux/linux-comm-crontab.html)
- [cron - How to prevent from CronJob run process twice? - Ask Ubuntu](https://askubuntu.com/questions/915690/how-to-prevent-from-cronjob-run-process-twice)
- [linux shell if 参数 - image eye - 博客园](https://www.cnblogs.com/image-eye/archive/2011/08/20/2147015.html)

