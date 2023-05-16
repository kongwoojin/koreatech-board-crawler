import edgedb
from fastapi.encoders import jsonable_encoder
from math import ceil

client = edgedb.create_async_client()


async def get_data(board: str, page: int, num_of_items: int):
    data = await client.query("""
            select sim 
            {num, title, writer, write_date, article_url} 
            filter .board=<str>$board order by contains(.num, '공지') desc 
            then .write_date desc
            then .num desc offset <int64>$offset limit <int64>$num_of_items
            """, board=board, offset=(page - 1) * num_of_items, num_of_items=num_of_items)

    count = await client.query("select count(sim filter sim.board=<str>$board)", board=board)

    return jsonable_encoder({"last_page": ceil(count[0] / num_of_items), "posts": data})


async def get_article(uuid: str):
    data = await client.query("""
            select sim 
            {title, writer, write_date, article_url, content, files}
            filter .id=<uuid>$uuid
            """, uuid=uuid)

    return data


async def sim_notice(page: int = 1, num_of_items: int = 20):
    return await get_data("373", page, num_of_items)
