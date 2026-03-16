from db import engine
from tables import user
from sqlalchemy import delete

def delete_user():
    with engine.connect() as conn:
        query = delete(user).where(user.c.age < 18)
        conn.execute(query)
        conn.commit()
