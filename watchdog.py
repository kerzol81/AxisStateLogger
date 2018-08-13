from axis import *
import time
import csv
import logging

today = datetime.date.today()
LOG_FORMAT = '%(levelname)s %(asctime)s %(message)s'
logging.basicConfig(filename='{}.log'.format(today), level=logging.INFO, format=LOG_FORMAT, datefmt='%Y:%m:%d %H:%M:%S')
logger = logging.getLogger()

freq = 300

logging.info('[+] Axis Watchdog started, refresh time: {} seconds'.format(freq))


while True:
    try:
        with open('config.csv', 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)

            for line in csv_reader:
                a = Axis(ip=str(line[0]).strip(), username=str(line[1]).strip(), password=str(line[2]).strip(), name=str(line[3]).strip())
    except:
        logging.error('[-] Axis Watchdog: no config file found')
        break

    time.sleep(freq)
