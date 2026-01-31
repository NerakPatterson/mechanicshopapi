from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache

# Base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass

# Database ORM
db = SQLAlchemy(model_class=Base)

# Serialization / deserialization
ma = Marshmallow()

# Database migrations
migrate = Migrate()

# Rate limiting (per client IP)
limiter = Limiter(key_func=get_remote_address)

# Caching (configured via app.config, e.g. CACHE_TYPE in .env or config.py)
cache = Cache()