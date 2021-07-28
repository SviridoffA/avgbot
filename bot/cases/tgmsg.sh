#!/bin/bash

token='507494875:AAFeukduhEpiFzHqvIK8Nf0nqDL5BeT5qlg'
#proxy='socks5h://avg:JlvbycjdctvFlby@bot.avangardpc.ru:7778'
chatid='-1001251699729'
chatid2='324248972'

#curl -s -x $proxy -G --data-urlencode "chat_id=$chatid" --data-urlencode "text=*$1*
#$2" --data-urlencode "parse_mode=Markdown" https://api.telegram.org/bot$token/sendMessage > /dev/null

curl -G --data-urlencode "chat_id=$chatid2" --data-urlencode "text=*$1*
$2" --data-urlencode "parse_mode=Markdown" https://api.telegram.org/bot$token/sendMessage > /dev/null
