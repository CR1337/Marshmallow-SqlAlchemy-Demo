from typing import Type

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from model import Address, User


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model: Type[User] = User
        include_relationships: bool = True
        load_instance: bool = True


class AddressSchema(SQLAlchemyAutoSchema):
    class Meta:
        model: Type[Address] = Address
        include_fk: bool = True
        load_instance: bool = True
