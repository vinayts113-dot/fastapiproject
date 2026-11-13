from sqlalchemy import text
from database import engine

try:
    with engine.connect() as connection:
        result =connection.execute(text("select  1"))
        print("database success")
        print(result.scalar())
except Exception as a:
    print("No sucess")
