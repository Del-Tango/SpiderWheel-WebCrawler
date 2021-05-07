#!/usr/bin/env python3
import time
import datetime
import shutil
import requests
import threading
import queue
import logging
import pysnooper
import re

from os import path, makedirs
from copy import copy
from lxml import etree
from lxml.html import iterlinks, resolve_base_href

from .sw_counter import Counter
from .sw_errors import HeaderError, SizeError
from .sw_robots_index import RobotsIndex
from .sw_thread_safe_set import ThreadSafeSet
from .sw_resources import ensure_directories_exist, ensure_files_exist

MIME_TYPES = {
    'application/atom+xml': '.atom',
    'application/epub+zip': '.epub',
    'application/font-woff': '.woff',
    'application/font-woff2': '.woff2',
    'application/force-download': '.bin',
    'application/gzip': '.gz',
    'application/java-archive': '.jar',
    'application/javascript': '.js',
    'application/js': '.js',
    'application/json': '.json',
    'application/json+oembed': '.json',
    'application/ld+json': '.jsonld',
    'application/marcxml+xml': '.mrcx',
    'application/msword': '.doc',
    'application/n-triples': '.nt',
    'application/octet-stream': '.exe',
    'application/ogg': '.ogx',
    'application/opensearchdescription+xml': '.osdx',
    'application/pdf': '.pdf',
    'application/postscript': '.eps',
    'application/rdf+xml': '.rdf',
    'application/rsd+xml': '.rsd',
    'application/rss+xml': '.rss',
    'application/txt': '.txt',
    'application/vnd.ms-cab-compressed': '.cab',
    'application/vnd.ms-excel': '.',
    'application/vnd.ms-fontobject': '.eot',
    'application/x-endnote-refer': '.enw',
    'application/x-www-form-urlencoded': '.png',
    'application/vnd.android.package-archive': '.apk',
    'application/vnd.oasis.opendocument.text': '.odt',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation': '.pptx',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
    'application/vnd.oasis.opendocument.formula-template': '.otf',
    'application/vnd.php.serialized': '.php',
    'application/x-bibtex': '.bib',
    'application/x-font-ttf': '.ttf',
    'application/x-font-woff': '.woff',
    'application/x-gzip': '.gz',
    'application/x-javascript': '.js',
    'application/x-mobipocket-ebook': '.mobi',
    'application/x-mpegurl': '.m3u8',
    'application/x-msi': '.msi',
    'application/x-research-info-systems': '.ris',
    'application/x-rss+xml': '.rss',
    'application/x-shockwave-flash': '.swf',
    'application/x-tar': '.tar.gz',
    'application/xhtml+xml': '.xhtml',
    'application/xml': '.xml',
    'application/zip': '.zip',
    'audio/mpeg': '.mp3',
    'audio/mp3': '.mp3',
    'audio/x-m4a': '.m4a',
    'binary/octet-stream': '.exe',
    'font/woff': '.woff', 'font/woff2': '.woff2',
    'font/ttf': '.ttf',
    'font/otf': '.otf',
    'html': '.html',
    'image/gif': '.gif',
    'image/jpeg': '.jpeg',
    'image/jpg': '.jpg',
    'image/pjpeg': '.jpg',
    'image/png': '.png',
    'image/ico': '.ico',
    'image/svg+xml': '.svg',
    'image/tiff': '.tif',
    'image/vnd.djvu': '.djvu',
    'image/vnd.microsoft.icon': '.ico',
    'image/webp': '.webp',
    'image/x-bitmap': '.xbm',
    'image/x-icon': '.ico',
    'image/x-ms-bmp': '.bmp',
    'text/calendar': '.ics',
    'text/css': '.css',
    'text/csv': '.csv',
    'text/directory': '.vcf',
    'text/html': '.html',
    'text/html,application/xhtml+xml,application/xml': '.html',
    'text/javascript': '.js',
    'text/n3': '.n3',
    'text/plain': '.txt',
    'text/turtle': '.ttl',
    'text/vnd.wap.wml': '.xml',
    'text/vtt': '.vtt',
    'text/x-c': '.c',
    'text/x-wiki': '.txt',
    'text/xml charset=utf-8': '.xml',
    'text/xml': '.xml',
    'video/3gpp': '.3gp',
    'video/3gp': '.3gp',
    'video/mp4': '.mp4',
    'video/webm': '.webp',
    'video/mpeg': '.mpeg',
    'video/x-flv': '.flv',
    'vnd.ms-fontobject': '.eot'
}

HEADERS = {
    'Chrome': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        '(KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'Accept-Language': 'en_US, en-US, en',
        'Accept-Encoding': 'gzip',
        'Connection': 'keep-alive'
    },
    'Firefox': {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:56.0) Gecko/20100101 Firefox/56.0',
        'Accept-Language': 'en_US, en-US, en',
        'Accept-Encoding': 'gzip',
        'Connection': 'keep-alive'
    },
    'IE': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Accept-Language': 'en_US, en-US, en',
        'Accept-Encoding': 'gzip',
        'Connection': 'keep-alive'
    },
    'Edge': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        '(KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063',
        'Accept-Language': 'en_US, en-US, en',
        'Accept-Encoding': 'gzip',
        'Connection': 'keep-alive'
    }
}

log = logging.getLogger(__name__)


#@pysnooper.snoop()
class SWWebCrawler():

    def __init__(self, *args, **kwargs):
        global log
        log = logging.getLogger(kwargs.get('log_name', __name__))
        self.follow_links = kwargs.get('follow_links', False)
        self.pattern_scout = kwargs.get('pattern_scout', True)
        self.search_pattern = kwargs.get('search_pattern', '[a-z]+')
        self.working_dir = kwargs.get('working_dir', path.realpath('.'))
        self.dump_file_path = kwargs.get(
            'dump_file_path', path.join(
                self.working_dir, 'dump', 'matched-pattern-files',
                'found-patterns-{}.out'.format(int(time.time()))
            )
        )
        self.start_time = int(time.time())
        self.start = kwargs.get(
            'start', ['https://en.wikipedia.org/wiki/Main_Page']
        )
        self.save_words = kwargs.get('save_words', True)
        self.save_count = kwargs.get('save_count', 1)
        self.max_new_errors = kwargs.get('max_new_errors', 1)
        self.max_known_errors = kwargs.get('max_known_errors', 20)
        self.max_http_errors = kwargs.get('max_http_errors', 50)
        self.max_new_mimes = kwargs.get('max_new_mimes', 10)
        self.respect_robots = kwargs.get('respect_robots', False)
        self.restrict = kwargs.get('restrict', False)
        self.domain = kwargs.get('domain', str())
        self.overwrite = kwargs.get('overwrite', True)
        self.raise_errors = kwargs.get('raise_errors', False)
        self.zip_files = kwargs.get('zip_files', True)
        self.override_size = kwargs.get('override_size', False)
        self.save_pages = kwargs.get('save_pages', False)
        self.saved_dir_path = kwargs.get('saved_dir_path', 'saved')
        self.todo_file = kwargs.get('todo_file', 'sw_web_crawler.todo')
        self.done_file = kwargs.get('done_file', 'sw_web_crawler.done')
        self.word_file = kwargs.get('word_file', 'sw_web_crawler.word')
        self.thread_count = kwargs.get('thread_count', 2)
        self.counter = Counter(0)
        self.new_error_count = Counter(0)
        self.known_error_count = Counter(0)
        self.http_error_count = Counter(0)
        self.new_mime_count = Counter(0)
        self.empty_counter = Counter(0)
        self.words = ThreadSafeSet()
        self.todo = queue.Queue()
        self.done = queue.Queue()
        self.thread_list = []
        self.save_mutex = threading.Lock()
        self.finished = False
        self.thread_running = True
        self.header = HEADERS[kwargs.get('header', 'Chrome')]

    # FETCHERS

#   @pysnooper.snoop()
    def fetch_matched_patterns_from_web_page(self, page, url):
        log.debug('')
        page_content = page.content.decode().split('\n')
        matched_patterns = []
        for page_line in page_content:
            try:
                check = re.search(
                    self.search_pattern, page_line, re.IGNORECASE
                )
                match = check.group()
            except:
                continue
            if check and match:
                matched_patterns.append(match)
        return list(set(matched_patterns))

    def fetch_mime_type(self, page):
        """
        [ NOTE ]: Extracts the Content-Type header from the headers
                  returned by page.
        """
        log.debug('')
        try:
            doc_type = str(page.headers['content-type'])
            return doc_type
        except KeyError:
            return ''

    def fetch_words_from_web_page(self, page):
        log.debug('')
        word_list = []
        if self.save_words:
            word_list = self.make_words(page)
            for word in word_list:
                self.words.put(word)
        return word_list

    def fetch_links_from_web_page(self, page):
        log.debug('')
        try:
            # [ NOTE ]: Pull out all links after resolving them using any
            #           <base> tags found in the document.
            links = [
                link for element, attribute, link, pos
                in iterlinks(resolve_base_href(page.content))
            ]
        except etree.ParseError:
            # [ NOTE ]: If the document is not HTML content this will return
            #           an empty list.
            links = []
        return list(set(links))

    # CRAWLERS

#   @pysnooper.snoop()
    def crawl(self, url, thread_id=0):
        log.debug('')
        if not self.override_size:
            self.check_page_too_large(url)
        # [ NOTE ]: If the SizeError is raised it will be caught in the except
        #           block in the run section, and the following code will not run.
        page = requests.get(url, headers=self.header)
        patterns = [] if not self.pattern_scout \
            else self.fetch_matched_patterns_from_web_page(page, url)
        if patterns:
            self.dump_matched_patterns_to_file(patterns, url)
        word_list = [] if not self.save_words \
            else self.fetch_words_from_web_page(page)
        links = [] if not self.follow_links \
            else self.fetch_links_from_web_page(page)
        if self.save_pages:
            self.save_page(url, page)
        # [ NOTE ]: Display which link was crawled
        if self.save_words:
            print('[ INFO ]: Worker({}) - Found {} links and {} words on {}'.format(thread_id, len(links), len(word_list), url))
        else:
            print('[ INFO ]: Worker({}) - Found {} links on {}'.format(thread_id, len(links), url))
        return links

#   @pysnooper.snoop()
    def crawl_worker(self, thread_id, robots_index):
        """
        [ NOTE ]: Crawler worker thread method
        """
        log.debug('')
        while self.thread_running:
            check_urls = self.check_urls_to_crawl()
            if not check_urls:
                return
            # [ NOTE ]: Queue not empty
            url = None
            try:
                # [ NOTE ]: If too many errors have occurred
                if self.new_error_count.val >= self.max_new_errors or \
                self.known_error_count.val >= self.max_known_errors or \
                self.http_error_count.val >= self.max_http_errors or \
                self.new_mime_count.val >= self.max_new_mimes:
                    print('[ ERROR ]: Too many errors have accumulated, stopping crawler.')
                    self.done_crawling()
                    break
                elif self.counter.val >= self.save_count:
                    # [ NOTE ]: If it's time for an autosave
                    save_files = self.make_sure_one_thread_saves_files(thread_id)
                else:
                    crawl_page = self.crawl_page(robots_index, thread_id)
                    if not crawl_page:
                        continue
            except KeyboardInterrupt:
                self.handle_keyboard_interrupt()
            except Exception as e:
                link = url
                print('[ INFO ]: Worker({}) - An error was raised trying to process {}'.format(thread_id, link))
                handle_error = self.handle_web_crawler_error(e, thread_id)
                # [ NOTE ]: Any other error
                if not handle_error:
                    self.new_error_count.increment()
                    print('[ ERROR ]: Worker({}) - An unknown error occured.'.format(thread_id))
                    if self.raise_errors:
                        self.done_crawling()
                        raise e
                    else:
                        continue
                print('[ INFO ]: Worker({}) - Saved error message and timestamp to error log file.'.format(thread_id))
                print('[ INFO ]: Worker({}) - Thread execution stopped.'.format(thread_id))
        return True

#   @pysnooper.snoop()
    def crawl_page(self, robots_index, thread_id):
        log.debug('')
        try:
            url = self.todo.get(block=False)
        except queue.Empty:
            return False
        else:
            if self.check_link(url, robots_index):
                # [ NOTE ]: If the link is invalid
                return False
            links = self.crawl(url, thread_id)
            for link in links:
                # [ NOTE ]: Skip empty links
                if len(link) <= 0 or link == "/":
                    continue
                # [ NOTE ]: If link is relative, make it absolute
                if link[0] == '/':
                    if url[-1] == '/':
                        link = url[:-1] + link
                    else:
                        link = url + link

                if self.follow_links:
                    self.todo.put(link)
            self.done.put(url)
            self.counter.increment()
            self.todo.task_done()
        return True

    # CHECKERS

    def check_urls_to_crawl(self):
        log.debug('')
        # [ NOTE ]: Check if there are more urls to crawl
        if self.todo.empty():
            # [ NOTE ]: Increment empty counter
            self.empty_counter.increment()
            # [ NOTE ]: Check if other threads are producing links
            #           by waiting till queue is empty
            while self.todo.empty():
                # [ NOTE ]: If all threads hit empty counter
                if self.empty_counter.val == self.thread_count:
                    self.done_crawling()
                    return False
                time.sleep(1)
            # [ NOTE ]: Got a url in queue, decrement counter
            self.empty_counter.decrement()
        return True

    def check_page_too_large(self, url):
        log.debug('')
        try:
            # [ NOTE ]: Attempt to get the size in bytes of the document
            length = int(requests.head(
                url, headers=self.header).headers['Content-Length'])
        except KeyError:
            # [ NOTE ]: Sometimes no Content-Length header is returned
            length = 1
        if length > 524288000:
            # [ NOTE ]: If the page is larger than 500 MB
            raise SizeError
        return False

    def check_link(self, item, robots_index=None):
        """
        [ RETURN ]: True if item is not a valid url, False otherwise.
        [ NOTE   ]: Shortest possible url ('http://a.b')
        [ NOTE   ]: Links longer than 255 characters are usually too long for
                    the filesystem to handle.
        """
        log.debug('')
        if robots_index and not robots_index.is_allowed(item):
            return True
        if self.restrict:
            if self.domain not in item:
                return True
        if len(item) < 10 or len(item) > 255:
            return True
        # [ NOTE ]: Must be an http(s) link
        elif item[0:4] != 'http':
            return True
        elif item in copy(self.done.queue):
            return True
        return False

    def check_word(self, word):
        """
        [ RETURN ]: True if word is not valid, False otherwise.
        [ NOTE   ]: If word is longer than 16 characters
                    (avg password length is ~8)
        """
        log.debug('')
        if len(word) > 16:
            return True
        else:
            return False

    def check_path(self, file_path):
        """
        [ RETURN ]: True if path is valid, False otherwise.
        [ NOTE   ]: Checks the path of a given filename to see whether it will
                    cause errors when saving.
        """
        log.debug('')
        if len(file_path) > 256:
            return False
        else:
            return True

    # CREATORS

    def create_dump_file(self):
        log.debug('')
        return ensure_files_exist(self.dump_file_path)

    def create_robots_index(self):
        log.debug('')
        robots_index = RobotsIndex(
            self.respect_robots, self.header['User-Agent'],
            log_name='SpiderWheel',
        )
        return robots_index

    def create_crawler_worker_threads(self):
        log.debug('')
        robots_index = self.create_robots_index()
        return self.spawn_threads(robots_index)

    def create_checkpoint_files(self):
        log.debug('')
        for start in self.start:
            self.todo.put(start)
        self.done = queue.Queue()
        return True

    # LOADERS

    def load_saved_todo_checkpoint_file(self):
        log.debug('')
        try:
            with open(self.todo_file, 'r', encoding='utf-8', errors='ignore') as f:
                contents = f.readlines()
        except FileNotFoundError:
            contents = []
        for line in contents:
            self.todo.put(line.strip())
        del contents
        return True

    def load_saved_done_checkpoint_file(self):
        log.debug('')
        try:
            with open(self.done_file, 'r', encoding='utf-8', errors='ignore') as f:
                contents = f.readlines()
        except FileNotFoundError:
            contents = []
        for line in contents:
            self.done.put(line.strip())
        del contents
        return True

    def load_checkpoint_files(self):
        log.debug('')
        print('[ INFO ]: Loading checkpoint files...')
        self.load_saved_todo_checkpoint_file()
        self.load_saved_done_checkpoint_file()
        # [ NOTE ]: If self.todo list is empty, add default starting pages
        if self.todo.qsize() == 0:
            for start in self.start:
                self.todo.put(start)
        return True

    # INIT

#   @pysnooper.snoop()
    def init(self):
        log.debug('')
        self.create_dump_file()
        if self.overwrite:
            return self.create_checkpoint_files()
        return self.load_checkpoint_files()

    # SPAWNERS

#   @pysnooper.snoop()
    def spawn_threads(self, robots_index):
        log.debug('')
        try:
            print('[ INFO ]: Spawning ({}) worker threads...'.format(self.thread_count))
            for i in range(self.thread_count):
                t = threading.Thread(
                    target=self.crawl_worker, args=(i+1, robots_index)
                )
                print('[ INFO ]: Worker({}) - Starting crawl...'.format(i+1))
                t.daemon = True
                t.start()
                self.thread_list.append(t)
            for t in self.thread_list:
                t.join()
        except KeyboardInterrupt:
            self.handle_keyboard_interrupt()

    # GENERAL

#   @pysnooper.snoop()
    def dump_matched_patterns_to_file(self, matched_patterns, url):
        log.debug('')
        banner = '\n-- {} --\n'.format(url)
        return self.update_file(
            self.dump_file_path, set(matched_patterns),
            'matched patterns', banner=banner
        )

    def make_words(self, site):
        """
        [ RETURN ]: List of all valid words in page.
        """
        log.debug('')
        # [ NOTE ]: Get page content
        page = site.text
        # [ NOTE ]: Split content into lists of words, as separated by spaces
        word_list = page.split()
        del page
        # [ NOTE ]: Remove duplicates
        word_list = list(set(word_list))
        for word in word_list:
            # [ NOTE ]: If word is invalid
            if self.check_word(word):
                # [ NOTE ]: Remove invalid word from list
                word_list.remove(word)
        return word_list

    def save_todo_file(self):
        log.debug('')
        with open(self.todo_file, 'w', encoding='utf-8', errors='ignore') \
                as todo_list:
            for site in copy(self.todo.queue):
                try:
                    todo_list.write(site + '\n')
                except UnicodeError:
                    continue
        print('[ INFO ]: Saved TODO list to ({})'.format(self.todo_file))
        return True

    def save_done_file(self):
        log.debug('')
        with open(self.done_file, 'w', encoding='utf-8', errors='ignore') \
                as done_list:
            for site in copy(self.done.queue):
                try:
                    done_list.write(site + '\n')
                except UnicodeError:
                    continue
        print('[ INFO ]: Saved DONE list to ({})'.format(self.done_file))
        return True

    def save_files(self):
        """
        [ NOTE ]: Saves the TODO, DONE, and WORDS lists into their
                  respective files.
        """
        log.debug('')
        self.save_todo_file()
        self.save_done_file()
        if self.save_words:
            self.update_file(self.word_file, self.words.get_all(), 'words')
        return True

    def make_file_path(self, url, ext):
        """
        [ NOTE ]: Makes a valid Windows file path for a given url.
        """
        log.debug('')
        # [ NOTE ]: Remove extension from path
        url = url.replace(ext, '')
        # [ NOTE ]: Remove illegal characters from path
        for char in """/\\ *""":
            url = url.replace(char, '-')
        for char in """|:?&<>""":
            url = url.replace(char, '')
        # [ NOTE ]: Truncate to valid file length
        url = url[:255] + ext
        return url

    def mime_lookup(self, value):
        """
        [ NOTE ]: Finds the correct file extension for a MIME type using the
                  MIME TYPES dictionary.
        [ NOTE ]: If the MIME type is blank it defaults to .html, and if the
                  MIME type is not in the dictionary it raises a HeaderError.
        """
        log.debug('')
        # [ NOTE ]: Reduce to lowercase
        value = value.lower()
        # [ NOTE ]: Remove possible encoding
        value = value.split(';')[0]
        if value in MIME_TYPES:
            return MIME_TYPES[value]
        elif value == '':
            return '.html'
        else:
            raise HeaderError('Unknown MIME type: {}'.format(value))

    def save_page(self, url, page):
        """
        [ NOTE ]: Download content of url and save to the save folder.
        """
        log.debug('')
        # [ NOTE ]: Make file path
        ext = self.mime_lookup(self.fetch_mime_type(page))
        cropped_url = self.make_file_path(url, ext)
        file_path = path.join(self.saved_dir_path, '{}'.format(cropped_url))
        # [ NOTE ]: Save file
        with open(file_path, 'w', encoding='utf-8', errors='ignore') as file:
            if ext == '.html':
                file.write(
                    '<!-- Regards, the Alveare Solutions society - "{}" -->\n'\
                    .format(url)
                )
            file.write(page.text)
        return True

#   @pysnooper.snoop()
    def update_file(self, target_file, content, file_type, banner=None):
        log.debug('')
        contents = []
        # [ NOTE ]: Open target file for reading and writing
        with open(target_file, 'r+', encoding='utf-8', errors='ignore') as open_file:
        # [ NOTE ]: Make list of all lines in file
            file_content = open_file.readlines()
            for x in file_content:
                contents.append(x.strip())
            for item in file_content:
                # [ NOTE ]: Otherwise add item to content (set)
                content.update(item)
            del file_content
            open_file.close()
        with open(target_file, 'a', encoding='utf-8', errors='ignore') as open_file:
            if isinstance(banner, str):
                open_file.write(banner)
            for item in content:
                # [ NOTE ]: Write all words to file
                open_file.write('\n' + str(item))
            # [ NOTE ]: Delete everything in file beyond what has been written
            if isinstance(banner, str):
                open_file.write(
                    '\n\n--- {} ---\n'.format(
                        datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
                    )
                )
            open_file.truncate()
        print('[ INFO ]: Saved {} {} to ({})'.format(len(content), file_type, target_file))
        return True

    def zip_saved_files(self, out_file_name, directory):
        log.debug('')
        shutil.make_archive(str(out_file_name), 'zip', directory)
        shutil.rmtree(directory)
        makedirs(directory)
        print('[ INFO ]: Zipped documents to ({}.zip)'.format(out_file_name))
        return True

    def make_sure_one_thread_saves_files(self, thread_id):
        log.debug('')
        with self.save_mutex:
            if self.counter.val <= 0:
                return False
            try:
                print('[ INFO ]: Worker({}) - Queried {} links.'.format(thread_id, str(self.counter.val)))
                print('[ INFO ]: Saving files...')
                self.save_files()
                if self.zip_files:
                    self.zip_saved_files(time.time(), self.saved_dir_path)
            finally:
                # [ NOTE ]: Reset variables
                self.counter = Counter(0)
                self.words.clear()
        return True

    def kill_threads(self):
        log.debug('')
        print('[ INFO ]: Stopping all threads...')
        self.thread_running = False

    def done_crawling(self, keyboard_interrupt=False):
        log.debug('')
        # [ NOTE ]: Make sure only one thread calls this
        with self.save_mutex:
            if self.finished:
                return
            self.kill_threads()
            self.finished = True
            if keyboard_interrupt:
                print('[ INFO ]: User performed a KeyboardInterrupt, stopping crawler.')
            else:
                print('[ INFO ]: Saving files...')
            self.save_files()

    # HANDLERS

    def handle_web_crawler_error(self, error, thread_id):
        log.debug('')
        err_mro = type(error).mro()
        if SizeError in err_mro:
            self.known_error_count.increment()
            print('[ ERROR ]: Worker({}) - Document too large.'.format(thread_id))

        elif OSError in err_mro:
            self.known_error_count.increment()
            print('[ ERROR ]: Worker({}) - An OSError occurred.'.format(thread_id))

        elif str(error) == 'HTTP Error 403: Forbidden':
            print('[ ERROR ]: Worker({}) - HTTP 403: Access Forbidden.'.format(thread_id))

        elif etree.ParserError in err_mro:
            # [ NOTE ]: Error processing html/xml
            self.known_error_count.increment()
            print('[ ERROR ]: Worker({}) - An XMLSyntaxError occurred.'.format(thread_id))

        elif requests.exceptions.SSLError in err_mro:
            # [ NOTE ]: Invalid SSL certificate
            self.known_error_count.increment()
            print('[ ERROR ]: Worker({}) - An SSLError occurred. Site is using an invalid certificate.'.format(thread_id))

        elif requests.exceptions.ConnectionError in err_mro:
            # [ NOTE ]: Error connecting to page
            self.known_error_count.increment()
            print('[ ERROR ]: Worker({}) - A ConnectionError occurred. There\'s something wrong with somebody\'s network.'.format(thread_id))

        elif requests.exceptions.TooManyRedirects in err_mro:
            # [ NOTE ]: Exceeded 30 redirects.
            self.known_error_count.increment()
            print('[ ERROR ]: Worker({}) - A TooManyRedirects error occurred. Page is probably part of a redirect loop.'.format(thread_id))

        elif requests.exceptions.ContentDecodingError in err_mro:
            # [ NOTE ]: Received response with content-encoding: gzip,
            #           but failed to decode it.
            self.known_error_count.increment()
            print('[ ERROR ]: Worker({}) - A ContentDecodingError occurred. Probably just a zip bomb.'.format(thread_id))

        elif 'Unknown MIME type' in str(error):
            self.new_mime_count.increment()
            print('[ ERROR ]: Worker({}) - Unknown MIME type: {}'.format(thread_id, str(error)[18:]))

    def handle_keyboard_interrupt(self):
        log.debug('')
        self.kill_threads()
        self.done_crawling(True)

    # MAIN

#   @pysnooper.snoop()
    def unleash(self):
        log.debug('')
        try:
            self.init()
        except Exception:
            raise SystemExit(1)
        ensure_directories_exist(self.saved_dir_path)
        ensure_files_exist(self.word_file)
        print('[ INFO ]: Successfully started Spider Wheel web crawler...')
        print('[ INFO ]: Using headers: {}'.format(self.header))
        return self.create_crawler_worker_threads()


if __name__ == '__main__':
    web_crawler = SWWebCrawler()
    web_crawler.unleash()

