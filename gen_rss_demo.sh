#! /bin/ash


TMP_RSS_LOCK="/tmp/rss.lock"
if [ -e $TMP_RSS_LOCK ]; then
    echo "Another instance of rss script is running. Aborting."
    exit
else
touch $TMP_RSS_LOCK

# run python script to update rss feed
RSS_ENGINE_PATH="/root/rss_feed/rss-engine"
REPO_PATH="/root/rss_feed/XinArkh.github.io/"
OUTPUT_PATH=${REPO_PATH}"rss/"

echo "--- updating rss feed... ---"
python ${RSS_ENGINE_PATH}gen_rss_demo.py -o $OUTPUT_PATH
echo "--- rss feed updated! ---"

# upload rss feed to github repo
CRTDIR=$(pwd)
CRTDATE=$(date "+%Y-%m-%d")

cd $REPO_PATH
echo "--- uploading rss feed... ---"
git pull
git add rss/*.xml
git commit -m "rss feed daily update: "$CRTDATE
git push
echo "--- rss feed updating done! ---"

cd $CRTDIR
rm $TMP_RSS_LOCK
fi
