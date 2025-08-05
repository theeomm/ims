from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from app.db.db import create_db
from app.dependencies import templates
from app.routers.inventory import router as inventory_routes
from app.routers.users import router as user_routes
from app.routers.auth import router as auth_routes
from app.routers.transactions import router as transactions_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Generate DB
    create_db()
    yield


app = FastAPI(lifespan=lifespan)


app.mount(
    "/assets",
    StaticFiles(directory="app/static"),
    name="static",
)

app.include_router(user_routes, prefix="/users", tags=["Users"])
app.include_router(inventory_routes, prefix="/inventory", tags=["Inventory"])
app.include_router(auth_routes, prefix="/auth", tags=["Authentication"])
app.include_router(transactions_routes, prefix="/transactions", tags=["Transactions"])


@app.get("/", name="home")
async def home(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("index.html", context)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
    )
