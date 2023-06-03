import edgedb
from fastapi.encoders import jsonable_encoder
from math import ceil

client = edgedb.create_async_client()


async def get_data(board: str, page: int, num_of_items: int):
    data = await client.query("""
            select ide 
            {num, title, writer, write_date} 
            filter .board=<str>$board order by contains(.num, '공지') desc 
            then .write_date desc
            then .num desc offset <int64>$offset limit <int64>$num_of_items
            """, board=board, offset=(page - 1) * num_of_items, num_of_items=num_of_items)

    count = await client.query("select count(ide filter ide.board=<str>$board)", board=board)

    return jsonable_encoder({"last_page": ceil(count[0] / num_of_items), "posts": data})


async def get_article(uuid: str):
    data = await client.query("""
            select ide 
            {title, writer, write_date, article_url, content, files: {file_name, file_uri}}
            filter .id=<uuid>$uuid
            """, uuid=uuid)

    return data


async def ide_notice(page: int = 1, num_of_items: int = 20):
    return await get_data("330", page, num_of_items)


async def ide_free_board(page: int = 1, num_of_items: int = 20):
    return await get_data("332", page, num_of_items)