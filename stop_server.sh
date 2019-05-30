#!/bin/sh
ps -ef|grep 554|awk '{print $2}'|xargs kill -9
rm ./rtsp.pid
