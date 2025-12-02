# app/users/schemas.py
from extensions import ma
from models import User

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True
        load_instance = True

user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Login schema: only email + password
class LoginSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True

    email = ma.auto_field()
    password = ma.auto_field()

login_schema = LoginSchema()
