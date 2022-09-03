from fastapi import FastAPI

from routers.v1 import api
from routers.v2 import mechanical, arch, school, dorm, mechatronics, sim, cse, ite, ide, emc

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
