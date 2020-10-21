#!/bin/bash
#set -ex
usage() (
   echo $0 -h [host] -p [port] -cuid [cuid]
)

host=bjyz-feed-tucheng280.bjyz
port=8680
cuid=1F9CA1488A7B6935181ECA5E936B7C51CF6E4069FFCTBMQJLMC

while getopts "h:p:cuid" arg
do
   case $arg in
    h) 
      host=$OPTARG
    ;;
    p)
      port=$OPTARG
    ;;
    cuid)
      cuid=$OPTARG
    ;;
    ?)
      usage
      exit
    ;;
   esac
done


curl --header "log-id:984523497" -d '{"user":{"cuid":"1F9CA1488A7B6935181ECA5E936B7C51CF6E4069FFCTBMQJLMC"}, "retrieval_num":100, "request_feature": {"refresh_type": "SMALL", "product": "BAIDUAPP", "refresh_timestamp": 1530761515067026, "ip": "111.16.164.19", "network": "1_0", "location": {"province": "", "city": "", "district": ""}, "user_agent": ""}, "use_request_feature_cache": false}' http://$host:$port/SegmentRetrievalService/Retrieve 
