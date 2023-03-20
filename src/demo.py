import os

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from schema import AddressSchema, UserSchema
from model import Address, Base, User


def get_session() -> Session:
    path = "db/db.sqlite3"
    db_exists = os.path.exists(path)
    engine = create_engine(f'sqlite:///{path}', echo=False)
    if not db_exists:
        Base.metadata.create_all(engine)
    session = Session(engine)
    if not db_exists:
        fill_db(session)
    return session


def fill_db(session: Session):
    spongebob = User(
        name="spongebob",
        fullname="Spongebob Squarepants",
        addresses=[Address(email_address="spongebob@sqlalchemy.org")],
    )
    sandy = User(
        name="sandy",
        fullname="Sandy Cheeks",
        addresses=[
            Address(email_address="sandy@sqlalchemy.org"),
            Address(email_address="sandy@squirrelpower.org"),
        ],
    )
    patrick = User(name="patrick", fullname="Patrick Star")
    session.add_all([spongebob, sandy, patrick])
    session.commit()


def get_users(session: Session) -> list[User]:
    stmt = select(User).where(User.name.in_(["spongebob", "sandy"]))
    return [user for user in session.scalars(stmt)]


def serialize_users(users: list[User]) -> list[str]:
    user_schema = UserSchema()
    return [user_schema.dump(user) for user in users]


def deserialize_users(users: list[str], session: Session) -> list[User]:
    user_schema = UserSchema()
    return [user_schema.load(user, session=session) for user in users]


def main():
    session = get_session()

    users = get_users(session)
    print(users)
    print()

    serialized_users = serialize_users(users)
    print(serialized_users)
    print()

    deserialized_users = deserialize_users(serialized_users, session)
    print(deserialized_users)
    print()


if __name__ == "__main__":
    main()
