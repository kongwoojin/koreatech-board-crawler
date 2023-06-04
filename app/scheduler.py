from rocketry import Rocketry
from rocketry.conds import every
from app.crawler.v3.main import main_crawler

app = Rocketry(execution="thread")


@app.task(every('3 hours', based="finish"))
async def crawler():
    main_crawler()


if __name__ == "__main__":
    app.run()
