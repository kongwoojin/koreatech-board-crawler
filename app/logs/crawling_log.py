import inspect
import os.path

from app.dataclass.board import Board


def attribute_exception_error(url, exception):
    caller = os.path.splitext(os.path.basename(inspect.stack()[1].filename))[0]
    print(f"{caller}: Failed to crawling {url} due to attribute error, {exception}")


def unknown_exception_error(exception):
    caller = os.path.splitext(os.path.basename(inspect.stack()[1].filename))[0]
    print(f"{caller}: {exception}")


def http_response_error(status, url):
    caller = os.path.splitext(os.path.basename(inspect.stack()[1].filename))[0]
    print(f"{caller}: {status} received when trying to crawling {url}")


def article_crawling_log(data: Board):
    caller = os.path.splitext(os.path.basename(inspect.stack()[1].filename))[0]
    print(f"{caller}: Start crawling article {data.num} from {data.board}...")


def board_crawling_log(board, page: int):
    caller = os.path.splitext(os.path.basename(inspect.stack()[1].filename))[0]
    print(f"{caller}: Start crawling {board} page {page}...")
