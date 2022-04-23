#/bin/bash

#Check network connection is OK:
attempts=0
tries=$1
while [ $attempts -lt $tries ]
do
  ping -c1 google.com >/dev/null 2>&1
  result=$?

  if [ $result -eq 0 ] #Successful network connection
  then
    sleep 3
    timedatectl status | grep synchronized | grep yes >/dev/null 2>&1
    result=$?
    if [ $result -eq 0 ] #network time synchronised!
    then
      exit 0
    else #Network time not synchronised - try and force it...
      sudo systemctl restart systemd-timedated >/dev/null 2>&1
      sleep 8
      timedatectl status | grep synchronized | grep yes >/dev/null 2>&1
      result=$?
      if [ $result -eq 0 ] #network time synchronised!
      then
        exit 0
      else
	sleep 8
        timedatectl status | grep synchronized | grep yes >/dev/null 2>&1
        result=$?
        if [ $result -eq 0 ] #network time synchronised!
        then
          exit 0
        else
          exit 1
	fi
      fi
    fi
  else
    if [ $tries -gt 1 ] #Only sleep here if trying more than once
    then
      sleep 2
    fi
    attempts=$[$attempts+1]
  fi
done
exit 2


