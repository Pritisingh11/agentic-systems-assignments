from db import engine
from sqlalchemy import MetaData, Table, Column, Integer, String, CheckConstraint

metadata = MetaData()
#user table
user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50), nullable = True),
    Column("age", Integer, CheckConstraint("age > 0")),
    Column("city", String(50), nullable = False)
)

def create_tables():
    metadata.create_all(engine)