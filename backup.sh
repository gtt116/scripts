#!/bin/bash
set -x
BACK_PREFIX='jenkins'
BACK_COUNT=7
BACK_PATH='/backup/'

timestamp=`date +'%Y_%m_%d.%H.%M.%S'`

tar czf ~/jenkins_backup.tar.gz \
            --exclude='var/lib/jenkins/logs/*' \
                    --exclude='/var/lib/jenkins/jobs/*/builds/*' \
                            /var/lib/jenkins/

cp jenkins_backup.tar.gz  ${BACK_PATH}/"${timestamp}_${BACK_PREFIX}.tar.gz"

cd $BACK_PATH
ls -t1 | tail -n+$((BACK_COUNT+1)) | xargs rm -rf
