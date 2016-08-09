小说的训练过程：
选正向词：
python fefilter.py -t novel_train_data.txt -c site_nav_data.txt
生成两个文件NOVEL_word_list.tmp NOVEL_word_prior_prob.tmp 
正向词一般看NOVEL_word_prior_prob.tmp
选负向词：
python fefilter.py -t nor_train_data.txt -c site_nav_data.txt
同样生成两个文件NOR_word_list.tmp NOR_word_prior_prob.tmp
负向词看NOR_word_list.tmp即可 参考NOR_word_prior_prob.tmp

训练：
python bayes_train.py -w all_fe_words.txt -t all_train_data.txt -m NOVEL 
产生一个 prior_prob.res.tmp 这个就是特征表
测试:
python bayes_test.py -p prior_prob.res.tmp -t novel_train_data.txt
python bayes_test.py -p prior_prob.res.tmp -t nor_train_data.txt

