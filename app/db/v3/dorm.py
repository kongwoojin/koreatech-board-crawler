import edgedb
from fastapi.encoders import jsonable_encoder
from math import ceil

client = edgedb.create_async_client()


async def get_data(board: str, page: int, num_of_items: int):
    try:
        data = await client.query("""
                select dorm 
                {num, title, writer, write_date, read_count} 
                filter .board=<str>$board order by contains(.num, '공지') desc 
                then .write_date desc
                then .num desc offset <int64>$offset limit <int64>$num_of_items
                """, board=board, offset=(page - 1) * num_of_items, num_of_items=num_of_items)

        count = await client.query("select count(dorm filter dorm.board=<str>$board)", board=board)

        return jsonable_encoder({"last_page": ceil(count[0] / num_of_items), "posts": data})
    except Exception:
        return jsonable_encoder({"error": "Unknown error!"})


async def get_article(uuid: str):
    try:
        data = await client.query("""
                select dorm 
                {title, writer, write_date, article_url, content, files: {file_name, file_uri}}
                filter .id=<uuid>$uuid
                """, uuid=uuid)

        return data
    except edgedb.errors.InvalidArgumentError:
        return jsonable_encoder({"error": "Wrong argument received!"})
    except Exception:
        return jsonable_encoder({"error": "Unknown error!"})


async def dorm_notice(page: int = 1, num_of_items: int = 20):
    return await get_data("notice", page, num_of_items)


async def dorm_free_board(page: int = 1, num_of_items: int = 20):
    return await get_data("bulletin", page, num_of_items)
