from pydantic import BaseModel,Field,ConfigDict

class ProductBase(BaseModel):

    name: str= Field(
        min_length=3,max_length=100
    )

    price : float =Field(gt=0, description ="Product price must be grater than 0")

    category : str=Field(min_length=3,max_length=100)

    stock:int

class ProductCreate(ProductBase):
        msg: str
        data: ProductBase

class ProductResponse(ProductBase):
        id:int