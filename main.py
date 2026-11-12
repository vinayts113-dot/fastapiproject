from fastapi import FastAPI 
from product import ProductCreate,ProductResponse

app=FastAPI()

@app.get("/greet")
def greeting():
    return "Hello small"

products = [
    {
        "id": 1,
        "name": "Laptop",
        "price": 65000,
        "category": "Electronics",
        "stock": 25
    },
    {
        "id": 2,
        "name": "Mobile",
        "price": 35000,
        "category": "Electronics",
        "stock": 40
    },
    {
        "id": 3,
        "name": "Keyboard",
        "price": 1800,
        "category": "Accessories",
        "stock": 15
    },
    {
        "id": 4,
        "name": "Mouse",
        "price": 750,
        "category": "Accessories",
        "stock": 30
    }
]



@app.get("/products")
def getproducts(id: str =None):
    if id:
        id=int(id)
        for p in products:
            if p["id"]==id:
                return p

        return {"msg":"Not found"}

    return products

@app.post("/addproduct",response_model=ProductResponse)
def addproduct(request: ProductCreate):
    new_id=max(p["id"] for p in products) +1 
    new_product={
     "id":new_id,
     **request.data.module_dump
    }
    products.append(new_product)
    return products