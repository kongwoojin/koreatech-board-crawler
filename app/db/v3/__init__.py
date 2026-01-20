import os
import json
from typing import Optional
from uuid import UUID, uuid4

import psycopg
from psycopg.rows import dict_row

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(usecwd=True))

postgres_host = os.getenv("POSTGRES_HOST")
postgres_port = os.getenv("POSTGRES_PORT")
postgres_user = os.getenv("POSTGRES_USER")
postgres_passwd = os.getenv("POSTGRES_PASSWORD")
postgres_dbname = os.getenv("POSTGRES_DB")


def get_connection():
    return psycopg.connect(
        host=postgres_host,
        port=postgres_port,
        user=postgres_user,
        password=postgres_passwd,
        dbname=postgres_dbname,
        row_factory=dict_row
    )


class PostgresClient:
    def __init__(self):
        self.conn = get_connection()

    def close(self):
        self.conn.close()

    def insert_notice(self, department: str, board: str, num: int, is_notice: bool,
                      title: str, writer: str, write_date, read_count: int,
                      article_url: str, content: str, crawled_time,
                      category: str = "NONE", file_data: Optional[str] = None) -> Optional[UUID]:
        """Insert a notice with files stored as JSONB. Returns notice id if inserted, None if updated."""
        with self.conn.cursor() as cur:
            # Parse file_data to store as JSONB
            files_json = json.loads(file_data) if file_data else None
            notice_id = uuid4()

            # Try to insert the notice
            cur.execute("""
                INSERT INTO notice (id, department, board, num, is_notice, category, title, writer,
                    write_date, read_count, notice_start_date, notice_end_date, article_url,
                    content, init_crawled_time, update_crawled_time, files)
                VALUES (%s, %s::department_enum, %s::board_enum, %s, %s, %s::category_enum, %s, %s, %s, %s, %s,
                    '9999-12-31', %s, %s, %s, %s, %s::jsonb)
                ON CONFLICT (article_url) DO UPDATE SET
                    title = EXCLUDED.title,
                    writer = EXCLUDED.writer,
                    is_notice = EXCLUDED.is_notice,
                    write_date = EXCLUDED.write_date,
                    read_count = EXCLUDED.read_count,
                    content = EXCLUDED.content,
                    update_crawled_time = EXCLUDED.update_crawled_time,
                    files = EXCLUDED.files
                RETURNING id, (xmax = 0) AS inserted
            """, (notice_id, department, board, num, is_notice, category, title, writer,
                  write_date, read_count, write_date, article_url, content,
                  crawled_time, crawled_time, json.dumps(files_json) if files_json else None))

            result = cur.fetchone()
            notice_id = result['id']
            was_inserted = result['inserted']

            self.conn.commit()
            return notice_id if was_inserted else None

    def update_notice_not_notice(self, department: str, board: str):
        """Set all notice articles to non-notice for a department/board."""
        with self.conn.cursor() as cur:
            cur.execute("""
                UPDATE notice
                SET is_notice = false
                WHERE department = %s::department_enum AND board = %s::board_enum AND is_notice = true
            """, (department, board))
            self.conn.commit()

    def get_articles(self, department: str, board: str, offset: int = 0,
                     limit: int = 20, is_notice: Optional[bool] = None,
                     only_new: bool = False):
        """Get articles with optional filtering."""
        with self.conn.cursor() as cur:
            conditions = ["department = %s::department_enum", "board = %s::board_enum"]
            params = [department, board]

            if is_notice is not None:
                conditions.append("is_notice = %s")
                params.append(is_notice)

            if only_new:
                conditions.append("init_crawled_time = update_crawled_time")

            where_clause = " AND ".join(conditions)

            cur.execute(f"""
                SELECT id, num, title, writer, write_date, read_count, is_notice, article_url,
                    (init_crawled_time = update_crawled_time) AS is_new
                FROM notice
                WHERE {where_clause}
                ORDER BY is_notice DESC, write_date DESC, num DESC
                OFFSET %s LIMIT %s
            """, params + [offset, limit])

            return cur.fetchall()

    def get_notice_articles(self, department: str, board: str):
        """Get all notice (pinned) articles."""
        return self.get_articles(department, board, is_notice=True)

    def get_article_count(self, department: str, board: str,
                          is_notice: Optional[bool] = None) -> int:
        """Get count of articles."""
        with self.conn.cursor() as cur:
            if is_notice is not None:
                cur.execute("""
                    SELECT COUNT(*) as count FROM notice
                    WHERE department = %s::department_enum AND board = %s::board_enum AND is_notice = %s
                """, (department, board, is_notice))
            else:
                cur.execute("""
                    SELECT COUNT(*) as count FROM notice
                    WHERE department = %s::department_enum AND board = %s::board_enum
                """, (department, board))

            return cur.fetchone()['count']

    def delete_notice(self, notice_id: UUID):
        """Delete a notice by ID."""
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM notice WHERE id = %s", (notice_id,))
            self.conn.commit()


def postgres_client():
    return PostgresClient()
