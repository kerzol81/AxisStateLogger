import requests
import datetime
import logging

today = datetime.date.today()
LOG_FORMAT = '%(levelname)s %(asctime)s %(message)s'
logging.basicConfig(filename='{}.log'.format(today), level=logging.INFO, format=LOG_FORMAT, datefmt='%Y:%m:%d %H:%M:%S')
logger = logging.getLogger()

class Axis:
    """ Axis camera class representing the state by pulling an image from the camera"""

    def __init__(self, ip='192.168.0.90', username='root', password='root', name='Axis'):
        self.ip = ip
        self.username = username
        self.password = password
        self.name = name
        self.base_url = 'http://{}:{}@{}/axis-cgi/'.format(username, password, ip)
        self.state = None
        self.get_state()

    def __str__(self):
        return '{} {} {}'.format(self.name, self.ip, self.state)

    def get_state(self):
        try:
            r = requests.get('http://{}:{}@{}/jpg/image.jpg'.format(self.username, self.password, self.ip), timeout=2)
            if r.status_code == 200:
                self.state = 'online'
                logging.info('{} @ online'.format(self.__str__()))
            elif r.status_code == 404:
                self.state = 'offline'
                logging.error('{} @ 404 error'.format(self.__str__()))
            elif r.status_code == 401:
                self.state = 'offline'
                logging.warning('{} @ authentication error'.format(self.__str__()))
            else:
                logging.error('{} @ unknown error'.format(self.__str__()))

        except:
            self.state = 'offline'
            logging.error('{} @ unreachable'.format(self.__str__()))

    def restart(self):
        try:
            r = requests.get('{}/restart.cgi'.format(self.base_url))
            if r.status_code == 200:
                logging.info('{} @ has been restarted'.format(self.__str__()))
        except:
            logging.error('{} @ was unable to restart'.format(self.__str__()))
