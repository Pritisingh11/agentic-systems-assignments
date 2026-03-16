from db import engine
from tables import user
from sqlalchemy import update

def update_user(name: str, city : str):
    with engine.connect() as conn:
        query = update(user).where(user.c.name == name).values(city = city)
        conn.execute(query)
        conn.commit()