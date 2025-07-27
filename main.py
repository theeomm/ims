from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from app.db.db import create_db
from app.dependencies import templates
from app.routers.items import router as items_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Generate DB
    create_db()
    yield


app = FastAPI(lifespan=lifespan)


app.mount("/assets", StaticFiles(directory="app/static"))
app.include_router(items_router)


@app.get("/")
async def home(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("index.html", context)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
    )
