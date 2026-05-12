from db import engine
from tables import user
from sqlalchemy import insert

#create user
def create_user (name : str, age: int, city: str):
    with engine.connect() as conn:
     query = insert(user).values(name = name, age = age, city = city)
     conn.execute(query)
     conn.commit()
    