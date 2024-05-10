import psycopg2

from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

engine = create_engine("sqlite:///db.sqlite3", echo=True)

# Connect to your postgres DB
conn = psycopg2.connect(
    dbname="email_telegram",
    user="postgres",
    password="2006",
    host="localhost",
    port="5432"
)

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a query
cur.execute('''
        CREATE TABLE IF NOT EXISTS info (
            id serial,
            name VARCHAR(30) not null,
            email varchar(30) not null,
            password varchar(30) not null
            )
    '''
            )


class Base(DeclarativeBase):
    pass


class UserForm(Base):
    __tablename__ = "info"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(String(30))

conn.commit()
