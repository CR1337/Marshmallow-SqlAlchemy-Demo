import os

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from model import Address, Base, User
from schema import AddressSchema, UserSchema

if __name__ == "__main__":
    if not os.path.exists('db/db.sqlite3'):
        from db_init import main as db_init_main
        db_init_main()
    engine = create_engine('sqlite:///db/db.sqlite3', echo=True)
    session = Session(engine)
