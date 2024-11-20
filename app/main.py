import time
from datetime import datetime

from fastapi import FastAPI, Request

from app.db import create_db_and_tables
from app.routes import customers, plans, transactions

app = FastAPI(
    lifespan=create_db_and_tables,
)

app.include_router(customers.router)
app.include_router(transactions.router)
app.include_router(plans.router)


@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    with open("log.txt", "a") as f:
        f.write(f"{request.method} {request.url} - {process_time}\n")
    print(f"LOG: {request.method} {request.url} - {process_time}")
    return response


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/date")
async def get_date():
    date = datetime.now()
    return {"date": f"Today is {date.strftime('%A, %B %d, %Y at %I:%M %p')}"}
