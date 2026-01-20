from app.dataclass.enums.board import Board
from app.dataclass.enums.department import Department
from app.db.v3 import postgres_client


def get_article_count(department: Department, board: str) -> int:
    client = postgres_client()
    try:
        return client.get_article_count(department.department, board)
    finally:
        client.close()


def get_notice_article_count(department: Department, board: str) -> int:
    client = postgres_client()
    try:
        return client.get_article_count(department.department, board, is_notice=True)
    finally:
        client.close()


if __name__ == '__main__':
    print(get_article_count(Department.CSE, Department.CSE.boards[0].board))
