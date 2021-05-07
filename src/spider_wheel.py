#!/usr/bin/env python3
#
# Regards, the Alveare Solutions society.
#
import pysnooper
import time
import optparse
import os

from sw_web_crawler.sw_resources import log_init
from sw_web_crawler.sw_web_crawler import SWWebCrawler

# COLD PARAMETERS

SCRIPT_NAME = 'SpiderWheel'
VERSION = 'v.Stalker'
VERSION_NUMBER = '1.0'
TIMESTAMP_FORMAT = '%d/%m/%Y-%H:%M:%S'
CURRENT_DIRECTORY = os.path.realpath('.')
LOG_FORMAT = '[ %(asctime)s ] %(name)s [ %(levelname)s ] %(thread)s - '\
    '%(filename)s - %(lineno)d: %(funcName)s - %(message)s'
RAISE_ERRORS = False
TODO_FILE = os.path.join(CURRENT_DIRECTORY, 'cache', 'sw_web_crawler.todo')
DONE_FILE = os.path.join(CURRENT_DIRECTORY, 'cache', 'sw_web_crawler.done')
WORD_FILE = os.path.join(CURRENT_DIRECTORY, 'cache', 'sw_web_crawler.word')
WEB_CRAWLER = None
SAVE_COUNT = 100
MAX_NEW_ERRORS = 1
MAX_KNOWN_ERRORS = 20
MAX_HTTP_ERRORS = 50
MAX_NEW_MIMES = 10

# HOT PARAMETERS

LOG_FILE_PATH = os.path.join(CURRENT_DIRECTORY, 'logs', 'spider-wheel.log')
PATTERN_SCOUT = True
SEARCH_PATTERN = '[a-z0-9]+'
CYCLE_COUNT = 0 # (0 | n)
DUMP_FILE = os.path.join(
    CURRENT_DIRECTORY, 'dump', 'matched-pattern-files',
    'pattern-scout-{}.out'.format(int(time.time()))
)
START = ['https://en.wikipedia.org/wiki/Main_Page']
SAVE_WORDS = False
RESPECT_ROBOTS = False
RESTRICT = False
RESTRICTED_DOMAIN = 'https://en.wikipedia.org'
OVERWRITE = True
ZIP_FILES = True
OVERRIDE_SIZE = False
SAVE_PAGES = False
SAVED_DIR_PATH = os.path.join(CURRENT_DIRECTORY, 'dump', 'saved-web-pages')
THREAD_COUNT = 2
HEADER = 'Chrome' # (Chrome | Firefox | IE | Edge)
FOLLOW_LINKS = False
CYCLE_INTERVAL = 5 # seconds
SILENT = False

log = log_init(LOG_FILE_PATH, LOG_FORMAT, TIMESTAMP_FORMAT, log_name=SCRIPT_NAME)

# FETCHERS

def fetch_web_crawler_creation_values():
    log.debug('')
    return {
        'log_name': SCRIPT_NAME,
        'pattern_scout': PATTERN_SCOUT,
        'search_pattern': SEARCH_PATTERN,
        'working_dir': CURRENT_DIRECTORY,
        'dump_file_path': DUMP_FILE,
        'start': START,
        'save_words': SAVE_WORDS,
        'save_count': SAVE_COUNT,
        'max_new_errors': MAX_NEW_ERRORS,
        'max_known_errors': MAX_KNOWN_ERRORS,
        'max_http_errors': MAX_HTTP_ERRORS,
        'max_new_mimes': MAX_NEW_MIMES,
        'respect_robots': RESPECT_ROBOTS,
        'restrict': RESTRICT,
        'domain': RESTRICTED_DOMAIN,
        'overwrite': OVERWRITE,
        'raise_errors': RAISE_ERRORS,
        'zip_files': ZIP_FILES,
        'override_size': OVERRIDE_SIZE,
        'save_pages': SAVE_PAGES,
        'saved_dir_path': SAVED_DIR_PATH,
        'todo_file': TODO_FILE,
        'done_file': DONE_FILE,
        'word_file': WORD_FILE,
        'thread_count': THREAD_COUNT,
        'header': HEADER,
        'follow_links': FOLLOW_LINKS,
    }

# CREATORS

def create_command_line_parser():
    log.debug('')
    parser = optparse.OptionParser(
        'Spider Wheel web crawler -\n\n%prog \ \n'
        '   -h | --help \ \n'
        '   -l | --log-file=         <FILE_PATH     type-(string)>   \n'
        '   -s | --search-pattern=   <REGEX         type-(string)>   \n'
        '   -d | --dump-file=        <FILE_PATH     type-(string)>   \n'
        '   -L | --load-url=         <START_URL     type-(string)>   \n'
        '   -u | --restricted-url=   <DOMAIN        type-(string)>   \n'
        '   -D | --saved-dir-path=   <DIR_PATH      type-(string)>   \n'
        '   -H | --header=           <HEADER        type-(string)>   \n'
        '   -c | --cyles=            <CYCLE_COUNT   type-(integer)>  \n'
        '   -t | --thread-count=     <THREADS       type-(integer)>  \n'
        '   -i | --cycle-interval=   <SECONDS       type-(integer)>  \n'
        '   -S | --pattern-scout                                     \n'
        '   -W | --save-words                                        \n'
        '   -R | --respect-robots                                    \n'
        '   -r | --restrict                                          \n'
        '   -o | --overwrite                                         \n'
        '   -z | --zip-files                                         \n'
        '   -O | --override-size                                     \n'
        '   -P | --save-pages                                        \n'
        '   -F | --follow-links                                      \n'
        '   -Q | --quiet                                             \n'
    )
    return parser

def create_web_crawler():
    log.debug('')
    creation_values = fetch_web_crawler_creation_values()
    web_crawler = SWWebCrawler(**creation_values)
    return web_crawler

# GENERAL

def clear_screen():
    log.debug('')
    return os.system('cls' if os.name == 'nt' else 'clear')

def stdout_msg(message):
    log.debug('')
    log.info(message)
    if not SILENT:
        print(message)
        return True
    return False

def unleash_web_crawler():
    global WEB_CRAWLER
    log.debug('')
    del WEB_CRAWLER
    WEB_CRAWLER = create_web_crawler()
    WEB_CRAWLER.unleash()
    return True

# DISPLAY

def display_banner():
    log.debug('')
    banner = '''
_______________________________________________________________________________

 *                      *        Spider Wheel       *                        *
____________________________________________________________v.Stalker__________
                    Regards, the Alveare Solutions society.
    '''
    print(banner)
    return True

# PROCESSORS

def process_log_file_argument(parser, options):
    global LOG_FILE_PATH
    log.debug('')
    file_path = options.log_file_path
    if file_path == None:
        log.warning(
            'No log file provided. '
            'Defaulting to ({}).'.format(LOG_FILE_PATH)
        )
        return False
    LOG_FILE_PATH = file_path
    stdout_msg(
        '[ + ]: Log file setup ({}).'.format(LOG_FILE_PATH)
    )
    return True

def process_search_pattern_argument(parser, options):
    global SEARCH_PATTERN
    log.debug('')
    regex_pattern = options.search_pattern
    if regex_pattern == None:
        log.warning(
            'No search regex pattern provided. '
            'Defaulting to ({}).'.format(SEARCH_PATTERN)
        )
        return False
    SEARCH_PATTERN = regex_pattern
    stdout_msg(
        '[ + ]: Regex pattern setup ({}).'.format(SEARCH_PATTERN)
    )
    return True

def process_cycles_argument(parser, options):
    global CYCLE_COUNT
    log.debug('')
    crawler_cycles = options.crawler_cycles
    if crawler_cycles == None:
        log.warning(
            'No web crawler cycle count provided. '
            'Defaulting to ({}).'.format(CYCLE_COUNT)
        )
        return False
    CYCLE_COUNT = crawler_cycles
    stdout_msg(
        '[ + ]: Web Crawler cycles setup ({}).'.format(CYCLE_COUNT)
    )
    return True

def process_dump_file_argument(parser, options):
    global DUMP_FILE
    log.debug('')
    file_path = options.dump_file_path
    if file_path == None:
        log.warning(
            'No file path provided to dump matched patterns into. '
            'Defaulting to ({}).'.format(DUMP_FILE)
        )
        return False
    DUMP_FILE = file_path
    stdout_msg(
        '[ + ]: Dump file setup ({}).'.format(DUMP_FILE)
    )
    return True

def process_load_url_argument(parser, options):
    global START
    log.debug('')
    start_url = options.load_start_url
    if start_url == None:
        log.warning(
            'No URL provided to start crawling. '
            'Defaulting to ({}).'.format(START)
        )
        return False
    START = [start_url]
    stdout_msg(
        '[ + ]: Target URL setup ({}).'.format(START)
    )
    return True

def process_restricted_domain_argument(parser, options):
    global RESTRICT
    log.debug('')
    restricted = options.restrict
    if restricted == None:
        log.warning(
            'Restricted crawl not specified. '
            'Defaulting to ({}).'.format(RESTRICT)
        )
        return False
    RESTRICT = restricted
    stdout_msg(
        '[ + ]: Restrict crawler setup ({}).'.format(RESTRICT)
    )
    return True

def process_saved_dir_path_argument(parser, options):
    global SAVED_DIR_PATH
    log.debug('')
    saved_dir_path = options.saved_dir_path
    if saved_dir_path == None:
        log.warning(
            'No directory path provided to save crawled web pages to. '
            'Defaulting to ({}).'.format(SAVED_DIR_PATH)
        )
        return False
    SAVED_DIR_PATH = saved_dir_path
    stdout_msg(
        '[ + ]: Save directory setup ({}).'.format(SAVED_DIR_PATH)
    )
    return True

def process_thread_count_argument(parser, options):
    global THREAD_COUNT
    log.debug('')
    thread_count = options.thread_count
    if thread_count == None:
        log.warning(
            'No number of threads specified for web crawler. '
            'Defaulting to ({}).'.format(THREAD_COUNT)
        )
        return False
    THREAD_COUNT = thread_count
    stdout_msg(
        '[ + ]: Crawler thread count setup ({}).'.format(THREAD_COUNT)
    )
    return True

def process_header_argument(parser, options):
    global HEADER
    log.debug('')
    header = options.header
    if header == None:
        log.warning(
            'No browser header specified for web crawler masquerade. '
            'Defaulting to ({}).'.format(HEADER)
        )
        return False
    HEADER = header
    stdout_msg(
        '[ + ]: Crawler masquerade header setup ({}).'.format(HEADER)
    )
    return True

def process_cycle_interval_argument(parser, options):
    global CYCLE_INTERVAL
    log.debug('')
    cycle_interval = options.interval
    if cycle_interval == None:
        log.warning(
            'No web crawler cycle interval provided. '
            'Defaulting to ({}).'.format(CYCLE_INTERVAL)
        )
        return False
    CYCLE_INTERVAL = cycle_interval
    stdout_msg(
        '[ + ]: Crawler cycle interval setup ({} seconds).'.format(CYCLE_INTERVAL)
    )
    return True

def process_pattern_scout_argument(parser, options):
    global PATTERN_SCOUT
    log.debug('')
    pattern_scout = options.pattern_scout
    if pattern_scout == None:
        log.warning(
            'Pattern scout trigger not specified. '
            'Defaulting to ({}).'.format(PATTERN_SCOUT)
        )
        return False
    PATTERN_SCOUT = pattern_scout
    stdout_msg(
        '[ + ]: Pattern scout setup ({}).'.format(PATTERN_SCOUT)
    )
    return True

def process_save_words_argument(parser, options):
    global SAVE_WORDS
    log.debug('')
    save_words = options.save_words
    if save_words == None:
        log.warning(
            'Word save trigger not specified. '
            'Defaulting to ({}).'.format(SAVE_WORDS)
        )
        return False
    SAVE_WORDS = save_words
    stdout_msg(
        '[ + ]: Word save setup ({}).'.format(SAVE_WORDS)
    )
    return True

def process_respect_robots_argument(parser, options):
    global RESPECT_ROBOTS
    log.debug('')
    respect = options.respect_robots
    if respect == None:
        log.warning(
            'Word save trigger not specified. '
            'Defaulting to ({}).'.format(RESPECT_ROBOTS)
        )
        return False
    RESPECT_ROBOTS = respect
    stdout_msg(
        '[ + ]: Word save setup ({}).'.format(RESPECT_ROBOTS)
    )
    return True

def process_restrict_argument(parser, options):
    global RESTRICT
    log.debug('')
    restrict = options.restrict
    if restrict == None:
        log.warning(
            'Domain restriction trigger not specified. '
            'Defaulting to ({}).'.format(RESTRICT)
        )
        return False
    RESTRICT = restrict
    stdout_msg(
        '[ + ]: Domain restriction setup ({}).'.format(RESTRICT)
    )
    return True

def process_overwrite_argument(parser, options):
    global OVERWRITE
    log.debug('')
    overwrite = options.overwrite
    if overwrite == None:
        log.warning(
            'Overwrite trigger not specified. '
            'Defaulting to ({}).'.format(OVERWRITE)
        )
        return False
    OVERWRITE = overwrite
    stdout_msg(
        '[ + ]: Overwrite setup ({}).'.format(OVERWRITE)
    )
    return True

def process_zip_files_argument(parser, options):
    global ZIP_FILES
    log.debug('')
    zip_files = options.zip_files
    if zip_files == None:
        log.warning(
            'File archiver trigger not specified. '
            'Defaulting to ({}).'.format(ZIP_FILES)
        )
        return False
    ZIP_FILES = zip_files
    stdout_msg(
        '[ + ]: Zip files setup ({}).'.format(ZIP_FILES)
    )
    return True

def process_override_size_argument(parser, options):
    global OVERRIDE_SIZE
    log.debug('')
    override_size = options.override_size
    if override_size == None:
        log.warning(
            'Override size trigger not specified. '
            'Defaulting to ({}).'.format(OVERRIDE_SIZE)
        )
        return False
    OVERRIDE_SIZE = override_size
    stdout_msg(
        '[ + ]: Override size setup ({}).'.format(OVERRIDE_SIZE)
    )
    return True

def process_save_pages_argument(parser, options):
    global SAVE_PAGES
    log.debug('')
    save_pages = options.save_pages
    if save_pages == None:
        log.warning(
            'Web page downloader trigger not specified. '
            'Defaulting to ({}).'.format(SAVE_PAGES)
        )
        return False
    SAVE_PAGES = save_pages
    stdout_msg(
        '[ + ]: Save pages setup ({}).'.format(SAVE_PAGES)
    )
    return True

def process_follow_links_argument(parser, options):
    global FOLLOW_LINKS
    log.debug('')
    follow_links = options.follow_links
    if follow_links == None:
        log.warning(
            'Link jumper trigger not specified. '
            'Defaulting to ({}).'.format(FOLLOW_LINKS)
        )
        return False
    FOLLOW_LINKS = follow_links
    stdout_msg(
        '[ + ]: Follow links setup ({}).'.format(FOLLOW_LINKS)
    )
    return True

def process_quiet_argument(parser, options):
    global SILENT
    log.debug('')
    quiet = options.quiet
    if quiet == None:
        log.warning(
            'Link jumper trigger not specified. '
            'Defaulting to ({}).'.format(SILENT)
        )
        return False
    SILENT = quiet
    if not SILENT:
        stdout_msg(
            '[ + ]: Silent setup ({}).'.format(SILENT)
        )
    return True

def process_command_line_options(parser):
    log.debug('')
    (options, args) = parser.parse_args()
    processed = {
        'log_file': process_log_file_argument(parser, options),
        'search_pattern': process_search_pattern_argument(parser, options),
        'cyles': process_cycles_argument(parser, options),
        'dump_file': process_dump_file_argument(parser, options),
        'load_url': process_load_url_argument(parser, options),
        'restricted_domain': process_restricted_domain_argument(parser, options),
        'saved-dir_path': process_saved_dir_path_argument(parser, options),
        'thread_count': process_thread_count_argument(parser, options),
        'header': process_header_argument(parser, options),
        'cycle_interval': process_cycle_interval_argument(parser, options),
        'pattern_scout': process_pattern_scout_argument(parser, options),
        'save_words': process_save_words_argument(parser, options),
        'respect_robots': process_respect_robots_argument(parser, options),
        'restrict': process_restrict_argument(parser, options),
        'overwrite': process_overwrite_argument(parser, options),
        'zip_files': process_zip_files_argument(parser, options),
        'override_size': process_override_size_argument(parser, options),
        'save_pages': process_save_pages_argument(parser, options),
        'follow_links': process_follow_links_argument(parser, options),
        'quiet': process_quiet_argument(parser, options),
    }
    return processed

# PARSER

def add_command_line_parser_options(parser):
    log.debug('')
    parser.add_option(
        '-l', '--log-file', dest='log_file_path', type='string',
        help='Path to the log file.', metavar='FILE_PATH'
    )
    parser.add_option(
        '-F', '--follow-links', dest='follow_links', action='store_true',
        help='Crawl every encountered link on all the web pages.'
    )
    parser.add_option(
        '-P', '--save-pages', dest='save_pages', action='store_true',
        help='Save crawled web pages to disk.'
    )
    parser.add_option(
        '-O', '--override-size', dest='override_size', action='store_true',
        help='Discard 500 MB size limit on web pages to crawl.'
    )
    parser.add_option(
        '-z', '--zip-files', dest='zip_files', action='store_true',
        help='Archive saved web pages using zip.'
    )
    parser.add_option(
        '-o', '--overwrite', dest='overwrite', action='store_true',
        help='Disregard cached crawler state, start fresh.'
    )
    parser.add_option(
        '-r', '--restrict', dest='restrict', action='store_true',
        help='Restrict crawler search to a certain domain name.'
    )
    parser.add_option(
        '-R', '--respect-robots', dest='respect_robots', action='store_true',
        help='Respect robots.txt.'
    )
    parser.add_option(
        '-W', '--save-words', dest='save_words', action='store_true',
        help='Save the words found in crawled web pages to disk.'
    )
    parser.add_option(
        '-S', '--pattern-scout', dest='pattern_scout', action='store_true',
        help='Search for a regex pattern in the crawled web pages.'
    )
    parser.add_option(
        '-i', '--cycle-interval', dest='interval', type='int',
        help='Crawler cycle interval in seconds. An interval of 0 is endless.',
        metavar='INTERVAL'
    )
    parser.add_option(
        '-H', '--header', dest='header', type='string',
        help='Browser to masquerade as.',
        metavar='(Chrome | Firefox | IE | Edge)'
    )
    parser.add_option(
        '-t', '--thread-count', dest='thread_count', type='int',
        help='Number of threads the web crawler can use.', metavar='THREAD_COUNT'
    )
    parser.add_option(
        '-D', '--saved-dir-path', dest='saved_dir_path', type='string',
        help='Path to the directory to save web pages in.', metavar='DIR_PATH'
    )
    parser.add_option(
        '-u', '--restricted-url', dest='domain', type='string',
        help='Domain/subdomain to restrict crawler to (can be http://, https://, etc).',
        metavar='DOMAIN'
    )
    parser.add_option(
        '-L', '--load-url', dest='load_start_url', type='string',
        help='Load a URL to arm web crawler with.', metavar='URL'
    )
    parser.add_option(
        '-d', '--dump-file', dest='dump_file_path', type='string',
        help='Path to the matched pattern dump file.', metavar='FILE_PATH'
    )
    parser.add_option(
        '-c', '--cycles', dest='crawler_cycles', type='int',
        help='Number of cycles for the web crawler.', metavar='CYCLE_COUNT'
    )
    parser.add_option(
        '-s', '--search-pattern', dest='search_pattern', type='string',
        help='Path to the log file.', metavar='REGEX'
    )
    parser.add_option(
        '-Q', '--quiet', dest='quiet', action='store_true',
        help='Suppress STDOUT messages.',
    )
    return parser

#@pysnooper.snoop()
def parse_command_line_arguments():
    log.debug('')
    parser = create_command_line_parser()
    add_command_line_parser_options(parser)
    return process_command_line_options(parser)

# INIT

#@pysnooper.snoop()
def init_spider_wheel():
    log.debug('')
    display_banner()
    cycles = 1
    while True:
        if CYCLE_COUNT > 0:
            if cycles >= CYCLE_COUNT:
                break
        delimiter_string = '[ SpiderWheel ]: Web crawler cycle ({}).'.format(cycles)
        if cycles != 1:
            delimiter_string = '\n' + delimiter_string
        print(delimiter_string)
        crawl = unleash_web_crawler()
        cycles += 1
        time.sleep(CYCLE_INTERVAL)

if __name__ == '__main__':
    parse_command_line_arguments()
    init_spider_wheel()

