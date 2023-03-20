from typing import List, Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """
    All classes that need persistent fields in the database should inherit from this.
    The engine needs this base class to deduce the tables it needs to build when
    creating the database.
    """
    pass


class User(Base):
    # a class representing a table in the database needs a tablename
    __tablename__: str = "user"
    # if you want to allow unmapped attributes, you need to set this to True
    __allow_unmapped__: bool = True

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    age: Mapped[Optional[int]]

    # am unmapped attribute needs a default value!
    gangname: str = ""

    # if you want to initialize unmapped attributes, you need to override __init__
    def __init__(self, gangname: str = "SpongeTheBob", *args, **kwargs) -> None:
        self.gangname = gangname
        super().__init__(*args, **kwargs)

    addresses: Mapped[List['Address']] = relationship(
        back_populates='user', cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r}, age={self.age!r}, gangname={self.gangname!r})"


class Address(Base):
    __tablename__: str = "address"

    id : Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))

    user: Mapped['User'] = relationship(back_populates='addresses')

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"