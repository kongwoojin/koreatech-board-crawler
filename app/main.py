from fastapi import FastAPI

from apscheduler.schedulers.background import BackgroundScheduler

from app.routers.v1 import api
# from app.routers.v2 import cse, sim, dorm, school, mechatronics, emc, ide, arch, mechanical, ite
from app.routers.v3 import cse, sim, dorm, school, mechatronics, emc, ide, arch, mechanical, ite

from app.crawler.v3.main import main_crawler_one, main_crawler_two

app = FastAPI()

app.include_router(cse.router)
app.include_router(arch.router)
app.include_router(dorm.router)
app.include_router(emc.router)
app.include_router(ide.router)
app.include_router(ite.router)
app.include_router(mechanical.router)
app.include_router(mechatronics.router)
app.include_router(school.router)
app.include_router(sim.router)

app.include_router(api.router)


@app.on_event('startup')
def start_crawler():
    sched = BackgroundScheduler()
    sched.add_job(main_crawler_one, 'cron', hour="*", minute=0)
    sched.add_job(main_crawler_two, 'cron', hour="*", minute=30)
    sched.start()

    print("Crawling started..")
