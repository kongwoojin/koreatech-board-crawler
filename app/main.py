from rocketry import Rocketry
from rocketry.conds import every

import sys
from os import path

sys.path.append(path.abspath('.'))

from app.crawler.v3.main import main_crawler

app = Rocketry(execution="async")


@app.task(every('3 hours', based="finish"))
async def crawler():
    await main_crawler()


if __name__ == "__main__":
    app.run()
