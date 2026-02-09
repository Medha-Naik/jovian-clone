import sqlalchemy
import os
from sqlalchemy import create_engine,text
from dotenv import load_dotenv


load_dotenv()
database_url=os.getenv('DATABASE_URL')
engine = create_engine(database_url)


def load_jobs_from_db():
    with engine.connect()as conn:
        result=conn.execute(text("select * from jobs"))
        result_all=result.all()
        jobs=[dict(row._mapping)for row in result_all]

    return jobs

def create_tables():
    with engine.connect() as conn:
        conn.execute(text("""
            Create table if not exists jobs(
                     id serial primary key,
                     location varchar(250),
                     title varchar(250),
                     responsibilities varchar (2000),
                     requirements varchar(2000))
        """))
        conn.commit()