#!/bin/bash

trap 'kill $process; exit' INT

GPIO_PATH=/sys/class/gpio
SW_PATH=/home/pi/stockcube
SETUP_DISK=/media/pi/SCSETUP
SETUP_PATH=/home/pi/Setup
TEST_DISK=/media/pi/SCTEST
TEST_PATH=$SW_PATH/test

#Import config (Colour map most importantly!)
source /config/cube.txt

echo "2" > $GPIO_PATH/export #SCL
echo "3" > $GPIO_PATH/export #SDA

echo "in" > $GPIO_PATH/gpio2/direction
echo "in" > $GPIO_PATH/gpio3/direction

echo "low" > $GPIO_PATH/gpio2/direction
echo "low" > $GPIO_PATH/gpio3/direction


read mode1 < $GPIO_PATH/gpio2/value
read mode2 < $GPIO_PATH/gpio3/value

await_setup=1 #default to showing welcome screen
check_network=1

readyfile=$SW_PATH/ready.txt

if [ -f $readyfile ]
then
  echo "Existing Stock Cube setup found"
#  if [ $mode1 -eq 1 ] || [ $mode2 -eq 1 ]
#  then
    await_setup=0 #Goes into run mode
#  else
#    echo "Mode 0 selected - entering setup mode"
#  fi
else
  echo "No existing Stock Cube setup found"
fi

while $TRUE
do

  read mode1 < $GPIO_PATH/gpio2/value
  read mode2 < $GPIO_PATH/gpio3/value

  #Switch mode 0, or no current setup file exists (eg when shipped):
  if ([ $mode1 -eq 0 ] && [ $mode2 -eq 0 ]) || [ $await_setup -eq 1 ]
  then
    if [ -e $SETUP_DISK ]
    then
      echo "Found setup disk"
      #Copy cube logs onto setup disk
      mkdir -p $SETUP_DISK/logs/cubeLogs/
      cp -r $SW_PATH/logs/* $SETUP_DISK/logs/cubelogs/
      #Copy all files from USB stick to relevant directories
      #Only copy software files over if current version < USB version
      source $SW_PATH/Version.py
      curr_version=$Version
      echo "Current version = $curr_version"

      if [ -e $SETUP_DISK/FACTORY_RESET/ ]
      then
        echo "Factory reset requested"
        logfile=reset_log_$(date +'%Y%m%d_%H%M')
        mkdir -p $SETUP_DISK/logs/
        echo "Starting factory reset from v$curr_version" > $SETUP_DISK/logs/$logfile.txt
        sudo -H -u pi /home/pi/recovery/factory_reset.sh >> $SETUP_DISK/logs/$logfile.txt 2>&1 &
        exit 99 #Exit with status 99 - which means factory reset requested
      fi #No new stockcube software on USB stick - run Cube setup

      if [ -e $SETUP_DISK/github/Software/ ] #This should only exist if USB tool has downloaded new version
      then
	source $SETUP_DISK/Setup/Version.py
        disk_version=$Version
        if (( $(echo "$disk_version > $curr_version" |bc -l) )); then
          echo "Software update available - copying update script into place and exiting startup"
          cp $SETUP_DISK/github/Software/Utils/update.py /home/pi/
          chmod a+x /home/pi/update.py
          logfile=update_log_$(date +'%Y%m%d_%H%M')
  	  mkdir -p $SETUP_DISK/logs/
          echo "Attempting Stock Cube update from $curr_version to $disk_version" > $SETUP_DISK/logs/$logfile.txt
          sudo -H -u pi /home/pi/update.py >> $SETUP_DISK/logs/$logfile.txt 2>&1 &
  	  exit 2 #Exit with status 2 - which means update available
        else
          echo "Same version of software on disk as Cube - ignoring"
        fi
      fi #No new stockcube software on USB stick - run Cube setup

      echo "Running Cube setup"
      mkdir -p $SETUP_PATH
      cp $SETUP_DISK/Setup/* $SETUP_PATH
      logfile=setup_log_$(date +'%Y%m%d_%H%M')
      mkdir -p $SETUP_DISK/logs/
      echo "Setting up Stock Cube version $curr_version" > $SETUP_DISK/logs/$logfile.txt
      sudo -H -u pi $SW_PATH/setup.py >> $SETUP_DISK/logs/$logfile.txt 2>&1
      echo 1 > $SW_PATH/ready.txt	#This is how Stock Cube knows there is a valid setup installed
      await_setup=0

    elif [ -e $TEST_DISK ]
    then
      echo "Found Test disk - running production test"
      mkdir -p $TEST_PATH
      cp $TEST_DISK/* $TEST_PATH
      chmod a+x $TEST_PATH/*
      sudo eject $TEST_DISK
      sudo $TEST_PATH/SCtest.sh
    else
      /home/pi/stockcube/led-image-viewer --led-rows=64 --led-cols=192 --led-rgb-sequence="$ColourMap" --led-pixel-mapper="Rotate:90" --led-brightness=70 /home/pi/stockcube/WelcomeScreen.bmp &
#      sudo -H -u pi $SW_PATH/show_logo.py
      process=$!
      disk_found=0
      while [ $disk_found -eq 0 ] && (([ $mode1 -eq 0 ] && [ $mode2 -eq 0 ]) || [ $await_setup -eq 1 ])
      do
        read mode1 < $GPIO_PATH/gpio2/value
        read mode2 < $GPIO_PATH/gpio3/value

        sleep 3
        if [ -e $SETUP_DISK ]
        then
           echo "Setup disk found"
           disk_found=1

        elif [ -e $TEST_DISK ]
        then
           echo "Test disk found"
           disk_found=1
        else
           echo "No disk found"
           disk_found=0
        fi
      done
      echo "Killing process $process"
      sudo kill -15 $process
      sleep 2
    fi
  fi

  #Mode 1 requested:
  if [ $mode1 -eq 1 ]
  then
    if [ $check_network -eq 1 ]
    then
      $SW_PATH/check_network_time.sh #Returns 0 if all OK, 1 if no time sync, 2 if no network...
      result=$?
      if [ $result -eq 0 ]
      then
        sudo -H -u pi python $SW_PATH/get_local_timezone.py
        sudo -H -u pi python $SW_PATH/check_api.py
        check_network=0
      else
        if [ $result -eq 2 ] #No internet connection
        then
          #Can't get correct time - tell user will run in offline mode, and set NYSE status to Closed
          echo "Closed" > /home/pi/nyse_status.txt
          sudo -H -u pi python /home/pi/stockcube/networkerror.py
        else #Network OK, time not updated
          echo "Closed" > /home/pi/nyse_status.txt
          sudo -H -u pi python /home/pi/stockcube/timeerror.py
        fi
      fi
    fi
    source $SETUP_PATH/mode1.py
    cp /home/pi/stocks_demo1.txt /home/pi/stocks_demo.txt
    $SW_PATH/SC_mode1 --led-rgb-sequence="$ColourMap" -b $modeBrightness &
    process=$!

    read mode1 < $GPIO_PATH/gpio2/value
    while [ $mode1 -eq 1 ]
    do
      sleep 3
      read mode1 < $GPIO_PATH/gpio2/value
    done

    read mode1 < $GPIO_PATH/gpio2/value
    read mode2 < $GPIO_PATH/gpio3/value

    kill $process
  fi

  #Mode 2 requested:
  if [ $mode2 -eq 1 ]
  then
    if [ $check_network -eq 1 ]
    then
      $SW_PATH/check_network_time.sh #Returns 0 if all OK, 1 if no time sync, 2 if no network...
      result=$?
      if [ $result -eq 0 ]
      then
        sudo -H -u pi python $SW_PATH/get_local_timezone.py
        check_network=0
      else
        #Can't get correct time - tell user will be running in demo mode? Pass new variable to tools to indicate not live prices?
        sudo -H -u pi python /home/pi/stockcube/timeerror.py
      fi
    fi
    source $SETUP_PATH/mode2.py
    cp /home/pi/stocks_demo2.txt /home/pi/stocks_demo.txt
    $SW_PATH/SC_mode2 --led-rgb-sequence="$ColourMap" -b $modeBrightness &
    process=$!

    read mode2 < $GPIO_PATH/gpio3/value
    while [ $mode2 -eq 1 ]
    do
      sleep 3
      read mode2 < $GPIO_PATH/gpio3/value
    done

    read mode1 < $GPIO_PATH/gpio2/value
    read mode2 < $GPIO_PATH/gpio3/value

    kill $process
  fi

  #sleep 1
done







