from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
ma = Marshmallow()
migrate = Migrate()
limiter = Limiter(key_func=get_remote_address) #creating and instance of Limiter
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})