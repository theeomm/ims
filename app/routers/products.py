from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from sqlmodel import select
from app.db.db import DbSession
from app.db.models.inventory import Product, Category
from app.dependencies import templates

router = APIRouter(default_response_class=HTMLResponse)


@router.get("/", name="products:list")
def product_page(request: Request):
    return templates.TemplateResponse(
        "pages/products.html", {"request": request}
    )


@router.get("/list", name="products:list")
def product_list_partial(request: Request, session: DbSession):
    products = session.exec(select(Product)).all()
    context = {"products": products, "request": request}
    return templates.TemplateResponse("partials/products/list.html", context=context)


@router.get("/new", name="products:new")
def product_form_partial(request: Request, session: DbSession):
    categories = session.exec(select(Category)).all()
    context = {"request": request, "categories": categories}
    return templates.TemplateResponse("partials/products/form.html", context=context)


@router.post("/create", name="products:create")
def product_create(
    session: DbSession,
    request: Request,
    name: str = Form(...),
    sku: str = Form(...),
    price: float = Form(...),
    category_id: int = Form(None),
):
    product = Product(
        name=name,
        sku=sku,
        price=price,
        category_id=category_id,
    )
    session.add(product)
    session.commit()
    session.refresh(product)

    # After creation, return updated product list
    products = session.exec(select(Product)).all()

    context = {
        "request": request,
        "products": products,
        "message": "Product created successfully!",
    }
    return templates.TemplateResponse("partials/products/list.html", context=context)
