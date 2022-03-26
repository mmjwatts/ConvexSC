#!/usr/bin/env python
import time
import sys
import os
import subprocess
import shutil

#Now write the check_prices.py file dependent on modes
file = open("/home/pi/test_check_prices.sh", "w")
file.write("#/bin/bash\n")
file.write("/home/pi/stockcube/check_network_time.sh 1\n")
file.write("nw_status=$?\n")
file.write("echo $nw_status > /home/pi/nw_status.txt\n")
file.write("if [ $nw_status -eq 0 ]\n")
file.write("then\n")
#Only run price checks if we have network connection!
file.write("python /home/pi/stockcube/check_watchlist.py\n")
file.write("python /home/pi/stockcube/check_portfolio.py\n")
file.write("python /home/pi/stockcube/check_etfs.py\n")
file.write("python /home/pi/stockcube/check_exchanges.py\n")
file.write("/home/pi/stockcube/nyse_status\n")
file.write("fi\n")
file.close()
