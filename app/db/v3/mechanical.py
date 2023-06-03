import edgedb
from fastapi.encoders import jsonable_encoder
from math import ceil

client = edgedb.create_async_client()


async def get_data(board: str, page: int, num_of_items: int):
    data = await client.query("""
            select mechanical 
            {num, title, writer, write_date} 
            filter .board=<str>$board order by contains(.num, '공지') desc 
            then .write_date desc
            then .num desc offset <int64>$offset limit <int64>$num_of_items
            """, board=board, offset=(page - 1) * num_of_items, num_of_items=num_of_items)

    count = await client.query("select count(mechanical filter mechanical.board=<str>$board)", board=board)

    return jsonable_encoder({"last_page": ceil(count[0] / num_of_items), "posts": data})


async def get_article(uuid: str):
    data = await client.query("""
            select mechanical 
            {title, writer, write_date, article_url, content, files: {file_name, file_uri}}
            filter .id=<uuid>$uuid
            """, uuid=uuid)

    return data


async def mechanical_notice(page: int = 1, num_of_items: int = 20):
    return await get_data("229", page, num_of_items)


async def mechanical_lecture_notice(page: int = 1, num_of_items: int = 20):
    return await get_data("230", page, num_of_items)


async def mechanical_free_board(page: int = 1, num_of_items: int = 20):
    return await get_data("232", page, num_of_items)