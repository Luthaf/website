#!/bin/bash
source credentials.sh
FTPURL="ftp://$USER:$PASS@$HOST"
LCD=".build/"
RCD="/www/"

rm -rf .build
cactus build

lftp -c "set ftp:list-options -a;
open '$FTPURL';
lcd $LCD;
cd $RCD;
mirror --reverse \
       --delete \
       --verbose"
