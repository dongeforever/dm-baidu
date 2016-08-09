#!/bin/bash
src="/home/users/liuzhendong01/sem-classifier/liuzhendong01/"
des="work@cp01-tmpbos-mo286.cp01.baidu.com:/home/work/liuzhendong01/DM_NLP/"

#scp -r /home/users/liuzhendong01/DM_NLP/*  work@dbl-tmpbos-mo286.dbl01.baidu.com:/home/work/liuzhendong01/DM_NLP/ 
scp -r $src"bin" $src"data" $src/*.sh $des
