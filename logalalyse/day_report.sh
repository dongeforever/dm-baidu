#!/bin/bash
day = `date -v -d "last-day" +"%Y-%m-%d"`
echo "start"


generate_report(){
        filename=`date +"%Y%m%d"`".report"
            if [ -f $filename ] ; then
                        echo "$filename does eist"
                            else
                                        mysqldump -uroot -pqmpyq --databases --master-data=2 --single-transaction --opt future > $filename
                                            fi
                                        }

                                        cd "/mnt/mysqldumps/"
                                        while [ 'a' = 'a' ]
                                        do
                                                if [ `date +'%H'` -eq '00' ]; then
                                                            echo 'yes'
                                                                    backup
                                                                        else
                                                                                    echo 'no'
                                                                                        fi
                                                                                            sleep 3000
                                                                                        done
