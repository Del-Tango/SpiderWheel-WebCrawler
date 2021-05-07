import urllib
import threading
import logging

from reppy.robots import Robots

log = logging.getLogger(__name__)


class RobotsIndex(object):

    def __init__(self, respect_robots, user_agent, **kwargs):
        global log
        log = logging.getLogger(kwargs.get('log_name', __name__))
        log.debug('')
        self.respect_robots = respect_robots
        self.user_agent = user_agent
        self.lock = threading.Lock()
        self.index = {}

    def is_allowed(self, start_url):
        log.debug('')
        if self.respect_robots:
            return self._lookup(start_url)
        else:
            return True

    def size(self):
        log.debug('')
        return len(self.index)

    def _lookup(self, url):
        log.debug('')
        hostname = urllib.parse.urlparse(url).hostname
        if hostname not in self.index.keys():
            with self.lock:
                if hostname not in self.index.keys():
                    self._remember(url)
        return self.index[hostname].allowed(url)

    def _remember(self, url):
        log.debug('')
        urlparsed = urllib.parse.urlparse(url)
        robots_url = url.replace(urlparsed.path, '/robots.txt')
        print('[ INFO ]: Reading robots.txt file at: {}'.format(robots_url))
        robots = Robots.fetch(robots_url)
        checker = robots.agent(self.user_agent)
        self.index[urlparsed.hostname] = checker


