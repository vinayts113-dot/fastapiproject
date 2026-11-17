from fastapi import FastAPI 
from product import ProductCreate,ProductResponse
from database import SessionLocal,SessionMs
from sqlalchemy import text
import re
from datetime import datetime

app=FastAPI()
db=SessionLocal()
db1=SessionMs()


@app.get("/biotrans")
def get_bio_trans(datee=None,code=None,ach=1):
    if not datee:
        datee=datetime.now().strftime('%Y-%m-%d')
    
    print(datee)    
    chk_date=datee

    if re.match(r'^\d{4}-\d{2}(-\d{2})?$',chk_date):
        chk_date=chk_date
    else:
        print("No proper date")
        return

    if ach==1:
        try:
            query="""SELECT 
                    MIN(Logtime) as s_logtime,
                    MAX(Logtime) as end_logtime,
                    MIN(DATEADD(MINUTE,-30,logtime)) as starttime,
                    MAX(DATEADD(MINUTE,-30,Logtime)) as endtime,
                    DATEDIFF(Minute,MIN(Logtime),MAX(Logtime)) as minutes,
                    concat(DATEDIFF(minute,MIN(Logtime),Max(Logtime))/60,':',DATEDIFF(minute,MIN(Logtime),MAX(Logtime))-DATEDIFF(minute,MIN(Logtime),MAX(Logtime))/60*60) as hr_min,
                    CAST(Employeecode as varchar(100)) as Employeecode,
                    CAST(Logdate as varchar(100)) as Logdate
                FROM biotransauz
                WHERE Logdate LIKE :date_pattern
                GROUP BY Employeecode, Logdate """
            res=db1.execute(text(query),{"date_pattern":(datee + '%')}) 
            print(query)
            rows=res.mappings().all()
            #data=[dict(rows) for r in rows]
            return{
                "success":True,
                "data":rows
            }
        finally:
            db1.close()
            # or can use "f{datee}%"



@app.get("/receipts")
def mbareceipts():
    try:
        result=db.execute(text("""select * from mba_receipts where auid like 'AIT26%' and type='package' limit 10"""))
        rows=result.mappings().all();
        for row in rows:
            print(dict(row))
    finally:
        db.close()


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