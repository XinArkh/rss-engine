#! /bin/bash


TMP_RSS_LOCK="/tmp/rss.lock"
if [ -e ${TMP_RSS_LOCK} ]; then
    echo "Another instance of rss script is running. Aborting."
    exit
else
touch $TMP_RSS_LOCK

# run python script to update rss feed
RSS_ENGINE_PATH="/root/rss/rss-engine/"
REPO_PATH="/root/rss/XinArkh.github.io/"
OUTPUT_PATH=${REPO_PATH}"rss/"

echo `date`
echo "--- updating rss feed... ---"
python ${RSS_ENGINE_PATH}run_script.py -o $OUTPUT_PATH
echo "--- rss feed updated! ---"

# upload rss feed to github repo
CRTDIR=$(pwd)
# CRTDATE=$(date "+%Y-%m-%d")
CRTDATE=$(date)

echo "--- uploading rss feed to github repo... ---"
cd $REPO_PATH
git pull
git add rss/*.xml
git commit -m "rss feed auto update: ${CRTDATE}"
git push
cd $CRTDIR
echo "--- rss feed uploaded! ---"
echo "--- rss feed auto update done! ---"
echo
echo

rm $TMP_RSS_LOCK
fi
