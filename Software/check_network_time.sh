#/bin/bash

#Check network connection is OK:
attempts=0
while [ $attempts -lt 5 ]
do
  ping -c1 google.com >/dev/null 2>&1
  result=$?

  if [ $result -eq 0 ] #Successful network connection
  then
    timedatectl status | grep synchronized | grep yes >/dev/null 2>&1
    result=$?
    if [ $result -eq 0 ] #network time synchronised!
    then
      exit 0
    else #Network time not synchronised - try and force it...
      echo "Restarting timedatectl to force sync"
      sudo systemctl restart systemd-timedated >/dev/null 2>&1
      sleep 2
      timedatectl status | grep synchronized | grep yes >/dev/null 2>&1
      result=$?
      if [ $result -eq 0 ] #network time synchronised!
      then
        exit 0
      else
        exit 1
      fi
    fi
  else
    echo "no network connection"
    sleep 2
    attempts=$[$attempts+1]
  fi
done
exit 2


