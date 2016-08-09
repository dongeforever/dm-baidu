#!/bin/bash
prefix="http://cp01-wise-tftest00-jx.cp01.baidu.com:8501/l=3/tc?srd=1&dict=21&debug_js=1&tc_source=1&src="

date="APP_"`date +%m_%d_%H_%M_%S`
mkdir $date
cd $date

# this step will crawl the page and mine the nav data
python ../bin/crawler.py -c ../data/h5_url.txt -p $prefix

#cat "crawler_output.txt" >tmp

# this step will train and test the Bayes Model
#python ../bin/bayes.py ../data/novel/novel_train_data.txt  tmp  ../data/novel/stop_word.list >result.txt

