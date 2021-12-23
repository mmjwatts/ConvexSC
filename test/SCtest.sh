#!/bin/bash
GPIO_PATH=/sys/class/gpio
TEST_PATH=/home/pi/stockcube/test/

#echo "2" > $GPIO_PATH/export #SCL
#echo "3" > $GPIO_PATH/export #SDA

#echo "in" > $GPIO_PATH/gpio2/direction
#echo "in" > $GPIO_PATH/gpio3/direction

#echo "low" > $GPIO_PATH/gpio2/direction
#echo "low" > $GPIO_PATH/gpio3/direction


read mode1 < $GPIO_PATH/gpio2/value
read mode2 < $GPIO_PATH/gpio3/value

brightness=70

while $TRUE
do

  read mode1 < $GPIO_PATH/gpio2/value
  read mode2 < $GPIO_PATH/gpio3/value

  if [ $mode1 -eq 1 ]
  then
    $TEST_PATH/led-image-viewer --led-rows=64 --led-cols=192 --led-rgb-sequence="BGR" --led-pixel-mapper="Rotate:90" --led-brightness=$brightness $TEST_PATH/Test2.bmp &
    process=$!

    read mode1 < $GPIO_PATH/gpio2/value  
    while [ $mode1 -eq 1 ]
    do
      sleep 3
      read mode1 < $GPIO_PATH/gpio2/value  
    done

    read mode1 < $GPIO_PATH/gpio2/value
    read mode2 < $GPIO_PATH/gpio3/value

    sudo kill -15 $process
  elif [ $mode2 -eq 1 ]
  then
    $TEST_PATH/led-image-viewer --led-rows=64 --led-cols=192 --led-rgb-sequence="BGR" --led-pixel-mapper="Rotate:90" --led-brightness=$brightness $TEST_PATH/TestDone.bmp &
    process=$!

    read mode2 < $GPIO_PATH/gpio3/value  
    while [ $mode2 -eq 1 ]
    do
      sleep 3
      read mode2 < $GPIO_PATH/gpio3/value  
    done

    read mode1 < $GPIO_PATH/gpio2/value
    read mode2 < $GPIO_PATH/gpio3/value

    sudo kill -15 $process
  else
    $TEST_PATH/led-image-viewer --led-rows=64 --led-cols=192 --led-rgb-sequence="BGR" --led-pixel-mapper="Rotate:90" --led-brightness=$brightness $TEST_PATH/Test0.bmp &
    process=$!

    read mode1 < $GPIO_PATH/gpio2/value
    read mode2 < $GPIO_PATH/gpio3/value
    sum=$(($mode1 + $mode2))
    while [ $sum -eq 0 ]
    do
      sleep 3
      read mode1 < $GPIO_PATH/gpio2/value
      read mode2 < $GPIO_PATH/gpio3/value
      sum=$(($mode1 + $mode2))
    done

    read mode1 < $GPIO_PATH/gpio2/value
    read mode2 < $GPIO_PATH/gpio3/value

    sudo kill -15 $process

  fi
done


