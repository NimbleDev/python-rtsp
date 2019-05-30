#!/bin/sh
#!/usr/bin/python

if [ "$1" != "debug" ];
then
   nohup python /www/python_rtsp_server/Server.py 554 > ./rtsp.log 2>1 &
else
    python /www/python_rtsp_server/Server.py 554
fi

