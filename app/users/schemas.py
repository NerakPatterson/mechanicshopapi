# app/users/schemas.py
from extensions import ma
from models import User

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True
        load_instance = True
        exclude = ("password_hash",)  # don’t expose password hashes

user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Login schema: only email + password (raw input, not DB fields)
class LoginSchema(ma.Schema):
    email = ma.Str(required=True)
    password = ma.Str(required=True)

login_schema = LoginSchema()
