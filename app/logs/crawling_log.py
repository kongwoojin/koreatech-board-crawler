import inspect
import os.path
import time

from app.dataclass.board import Board


def attribute_exception_error(url, exception):
    caller = os.path.splitext(os.path.basename(inspect.stack()[1].filename))[0]
    print("{} {:<24}: Failed to crawling {} due to attribute error, {}".format(current_time(), caller, url, exception))


def unknown_exception_error(exception):
    caller = os.path.splitext(os.path.basename(inspect.stack()[1].filename))[0]
    print("{} {:<24}: {}".format(current_time(), caller, exception))


def http_response_error(status, url):
    caller = os.path.splitext(os.path.basename(inspect.stack()[1].filename))[0]
    print("{} {:<24}: {} received when trying to crawling {}".format(current_time(), caller, status, url))


def article_crawling_log(data: Board):
    caller = os.path.splitext(os.path.basename(inspect.stack()[1].filename))[0]
    print("{} {:<24}: Start crawling article {} of {}".format(current_time(), caller, data.num, data.board))


def board_crawling_log(board):
    caller = os.path.splitext(os.path.basename(inspect.stack()[1].filename))[0]
    print("{} {:<24}: Failed to get last page of {}".format(current_time(), caller, board))



def unknown_last_page_error(board):
    caller = os.path.splitext(os.path.basename(inspect.stack()[1].filename))[0]
    print("{} {:<24}: Failed to crawling {} due to attribute error, {}".format(current_time(), caller, url, exception))



def current_time():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
