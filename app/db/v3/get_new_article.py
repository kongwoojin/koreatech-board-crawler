from app.dataclass.enums.department import Department
from app.db.v3 import postgres_client
from app.logs.message_log import cannot_get_article_list


def get_new_articles(department: Department, board: str):
    client = postgres_client()
    try:
        new_articles = client.get_articles(
            department=department.department,
            board=board,
            offset=0,
            limit=20,
            only_new=True
        )
        return list(new_articles)
    except Exception as e:
        cannot_get_article_list(department, board, e)
        return list()
    finally:
        client.close()
