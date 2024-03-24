from app.dataclass.enums.board import Board
from app.dataclass.enums.department import Department
from app.db.v3 import edgedb_client


def get_article_count(department: Department, board: Board) -> int:
    client = edgedb_client()

    count = client.query("SELECT count(notice filter .department=<Department><str>$department AND "
                         ".board=<Board><str>$board)",
                         department=department.department, board=board.board)

    return int(count[0])


if __name__ == '__main__':
    print(get_article_count(Department.CSE, Board.NOTICE))
