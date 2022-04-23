#!/bin/bash

trap 'kill $process; exit' INT

GPIO_PATH=/sys/class/gpio
SW_PATH=/home/pi/stockcube
SETUP_DISK=/media/pi/SCSETUP
SETUP_PATH=/home/pi/Setup
UPDATE_PATH=/home/pi/update
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
  await_setup=0 #Goes into run mode
else
  echo "No existing Stock Cube setup found"
fi

#Check for phantom SCSETUP directory and remove if present!
if [ -e $SETUP_DISK ]
then
  #This checks if there are any files or folders within $SETUP disk directory
  #If not, it's a phantom and we should delete it so USB stick can be mounted
  contents='ls $SETUP_DISK | wc -l'
  if [ $contents -eq 0 ]
  then
    rm -rf $SETUP_DISK
  fi
fi

while $TRUE
do

  read mode1 < $GPIO_PATH/gpio2/value
  read mode2 < $GPIO_PATH/gpio3/value

  #Switch mode 0, or no current setup file exists (eg when shipped):
  if (([ $mode1 -eq 0 ] && [ $mode2 -eq 0 ]) || [ $await_setup -eq 1 ])
  then
    if [ -e $SETUP_DISK ]
    then
      echo "Found setup disk"
      #Copy cube logs onto setup disk
      mkdir -p $SETUP_DISK/logs/cubeLogs/
      ifconfig wlan0 > $SW_PATH/logs/wireless_info.txt
      cp -r $SW_PATH/logs/* $SETUP_DISK/logs/cubelogs/
      cp -r /home/pi/recovery/logs/* $SETUP_DISK/logs/cubelogs/
      #Copy all files from USB stick to relevant directories
      #Only copy software files over if current version < USB version
      source $SW_PATH/Version.py
      curr_version=$Version
      curr_app_version=$AppVersion
      echo "Current version = $curr_version"

      if [ -e $SETUP_DISK/FACTORY_RESET/ ]
      then
        echo "Factory reset requested"
        logfile=reset_log_$(date +'%Y%m%d_%H%M')
        sudo -H -u pi mkdir -p /home/pi/recovery/logs/
        sudo -H -u pi echo "Starting factory reset from v$curr_version" > /home/pi/recovery/logs/$logfile.txt
        sudo -H -u pi /home/pi/recovery/factory_reset.sh >> /home/pi/recovery/logs/$logfile.txt 2>&1 &
        exit 99 #Exit with status 99 - which means factory reset requested
      fi #No new stockcube software on USB stick - run Cube setup

      if [ -e $SETUP_DISK/Setup/github/Software/ ] #This should only exist if USB tool has downloaded new version
      then
	source $SETUP_DISK/Setup/github/Software/Version.py
        disk_version=$Version
        if awk "BEGIN {exit !($disk_version > $curr_version)}"; then
	  if [ -e $UPDATE_PATH ]
	  then
	     rm -rf $UPDATE_PATH
	  fi
	  cp -r $SETUP_DISK/Setup/github/Software $UPDATE_PATH
	  #Copy new version info back onto USB (this assumes following all runs OK, but that feels fair...)
	  cp $SETUP_DISK/Setup/github/Software/Version.py $SETUP_DISK/Setup/
	  rm -rf $SETUP_DISK/Setup/github/
	  chmod a+rwx $UPDATE_PATH/*
          sleep 2
          umount -f $SETUP_DISK
          echo "Software update available - copying update script into place and exiting startup"
          cp $UPDATE_PATH/update.py /home/pi/
          chmod a+x /home/pi/update.py
          logfile=update_log_$(date +'%Y%m%d_%H%M')
          echo "Attempting Stock Cube update from $curr_version to $disk_version" > $SW_PATH/logs/$logfile.txt
          sudo -H -u pi /home/pi/update.py >> $SW_PATH/logs/$logfile.txt 2>&1 &
  	  exit 2 #Exit with status 2 - which means update available
        else
          echo "Same version of software on disk as Cube - ignoring"
        fi
      fi #No new stockcube software on USB stick - run Cube setup

      echo "Running Cube setup"
      mkdir -p $SETUP_PATH
      cp $SETUP_DISK/Setup/* $SETUP_PATH
      sleep 2
      umount -f $SETUP_DISK
      logfile=setup_log_$(date +'%Y%m%d_%H%M')
      echo "Setting up Stock Cube version $curr_version" > $SW_PATH/logs/$logfile.txt
      sudo -H -u pi $SW_PATH/setup.py >> $SW_PATH/logs/$logfile.txt 2>&1
      #force a /home/pi/check_prices.sh to ensure there are all files required for running modes before we switch!
      sudo -H -u pi /home/pi/check_prices.sh
      echo 1 > $SW_PATH/ready.txt	#This is how Stock Cube knows there is a valid setup installed
      await_setup=0

    elif [ -e $TEST_DISK ]
    then
      echo "Found Test disk - running production test"
      mkdir -p $TEST_PATH
      cp $TEST_DISK/* $TEST_PATH
      chmod a+x $TEST_PATH/*
      umount $TEST_DISK
      sudo $TEST_PATH/SCtest.sh
    else
      /home/pi/stockcube/led-image-viewer --led-rows=64 --led-cols=192 --led-rgb-sequence="$ColourMap" --led-pixel-mapper="Rotate:90" --led-brightness=70 /home/pi/stockcube/WelcomeScreen.bmp &
#      sudo -H -u pi $SW_PATH/show_logo.py
      process=$!
      disk_found=0
      setup_waits=0
      while [ $disk_found -eq 0 ] && (([ $mode1 -eq 0 ] && [ $mode2 -eq 0 ]) || [ $await_setup -eq 1 ])
      do
        read mode1 < $GPIO_PATH/gpio2/value
        read mode2 < $GPIO_PATH/gpio3/value
	setup_waits=$[$setup_waits+1]	#Increment setup waits
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
	   if [ $setup_waits -eq 20 ] #Turns screens off after 60 seconds
	   then
             sudo kill -15 $process
             sudo pkill -u daemon
             sudo -H -u pi python /home/pi/stockcube/sleepinfo.py
	   fi
        fi
      done
      echo "Killing process $process"
      sudo kill -15 $process
      sudo pkill -u daemon
      sleep 2
    fi
  fi

  #Mode 1 requested:
  if [ $mode1 -eq 1 ] && [ $await_setup -eq 0 ]
  then
    nw_mode=0
    show_clock=0
    scrolling=1 #Default to scrolling mode
    source $SETUP_PATH/mode1.py #If variables above exist in this setup file, this overwrites them with setup values
    if [ $check_network -eq 1 ]
    then
      sudo -H -u pi python /home/pi/stockcube/networkinfo.py &
      $SW_PATH/check_network_time.sh 20 #Returns 0 if all OK, 1 if no time sync, 2 if no network...
      result=$?
      sudo pkill -f networkinfo
      if [ $result -eq 0 ]
      then
        sudo -H -u pi python $SW_PATH/check_api.py
        check_network=0
      else
        if [ $result -eq 2 ] #No internet connection
        then
          #Can't get correct time - tell user will run in offline mode, and set NYSE status to Closed
          echo "Closed" > /home/pi/nyse_status.txt
          sudo -H -u pi python /home/pi/stockcube/networkerror.py &
	  process=$!
        else #Network OK, time not updated
          echo "Closed" > /home/pi/nyse_status.txt
          sudo -H -u pi python /home/pi/stockcube/timeerror.py
	  check_network=0
	  nw_mode=1 #Force display of network status on top screen
        fi
      fi
    fi
    #If check_network is still 1, there is a network issue so leave screens driven by networkerror.py
    if [ $check_network -eq 0 ] #This is either 0 already, or has been changed by checks above
    then
      nice -n -20 $SW_PATH/SC_mode1 --led-rgb-sequence="$ColourMap" -b $modeBrightness -n $nw_mode -c $show_clock -s $scrolling &
      process=$!
    fi

    read mode1 < $GPIO_PATH/gpio2/value
    while [ $mode1 -eq 1 ]
    do
      sleep 3
      read mode1 < $GPIO_PATH/gpio2/value
    done

    read mode1 < $GPIO_PATH/gpio2/value
    read mode2 < $GPIO_PATH/gpio3/value

    kill $process
    sudo pkill -u daemon
    sudo pkill -f networkerror
  fi

  #Mode 2 requested:
  if [ $mode2 -eq 1 ] && [ $await_setup -eq 0 ]
  then
    nw_mode=0
    show_clock=0
    scrolling=1
    source $SETUP_PATH/mode2.py #If variables above exist in this setup file, this overwrites them with setup values
    if [ $check_network -eq 1 ]
    then
      sudo -H -u pi python /home/pi/stockcube/networkinfo.py &
      $SW_PATH/check_network_time.sh 20 #Returns 0 if all OK, 1 if no time sync, 2 if no network...
      result=$?
      sudo pkill -f networkinfo
      if [ $result -eq 0 ]
      then
        sudo -H -u pi python $SW_PATH/check_api.py
        check_network=0
      else
        if [ $result -eq 2 ] #No internet connection
        then
          #Can't get correct time - tell user will run in offline mode, and set NYSE status to Closed
          echo "Closed" > /home/pi/nyse_status.txt
          sudo -H -u pi python /home/pi/stockcube/networkerror.py &
	  process=$!
        else #Network OK, time not updated
          echo "Closed" > /home/pi/nyse_status.txt
          sudo -H -u pi python /home/pi/stockcube/timeerror.py
	  check_network=0
	  nw_mode=1 #Force display of network status on top screen
        fi
      fi
    fi
    #If check_network is still 1, there is a network issue so leave screens driven by networkerror.py
    if [ $check_network -eq 0 ] #This is either 0 already, or has been changed by checks above
    then
      nice -n -20 $SW_PATH/SC_mode2 --led-rgb-sequence="$ColourMap" -b $modeBrightness -n $nw_mode -c $show_clock -s $scrolling &
      process=$!
    fi

    read mode2 < $GPIO_PATH/gpio3/value
    while [ $mode2 -eq 1 ]
    do
      sleep 3
      read mode2 < $GPIO_PATH/gpio3/value
    done

    read mode1 < $GPIO_PATH/gpio2/value
    read mode2 < $GPIO_PATH/gpio3/value

    kill $process
    sudo pkill -u daemon
    sudo pkill -f networkerror
  fi

  #sleep 1
done







