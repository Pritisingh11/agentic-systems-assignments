from db import engine
from tables import user


def fetch_user():
    with engine.connect() as conn:
        query = user.select()
        data = conn.execute(query).fetchall()
        for row in data:
            print(row)