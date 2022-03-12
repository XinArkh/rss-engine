#! /bin/ash


TMP_RSS_LOCK="/tmp/rss.lock"
if [ -e $TMP_RSS_LOCK ]; then
    echo "Another instance of rss script is running. Aborting."
    exit
else
touch $TMP_RSS_LOCK

# run rss engine to generate xml file
ZJU_ME_PATH="/root/rss_feed/zju-me-rss/"
ZJU_GRS_PATH="/root/rss_feed/zju-grs-rss/"
REPO_PATH="/root/rss_feed/XinArkh.github.io/"
OUTPUT_PATH=${REPO_PATH}"rss/"

echo "--- updating zju-me rss feed... ---"
python ${ZJU_ME_PATH}rss_engine.py -o $OUTPUT_PATH
echo "--- updating zju-grs rss feed... ---"
python ${ZJU_GRS_PATH}rss_engine.py -o $OUTPUT_PATH


# upload xml to github repo
CRTDIR=$(pwd)
CRTDATE=$(date "+%Y-%m-%d")

cd $REPO_PATH
echo "--- uploading rss feed... ---"
git pull
git add rss/*.xml
git commit -m "rss daily update "$CRTDATE
git push
echo "--- rss feed updating done! ---"

cd $CRTDIR
rm $TMP_RSS_LOCK
fi
