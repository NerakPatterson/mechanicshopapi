from app import create_app
from config import ProductionConfig

# Create the app using ProductionConfig for Render deployment
app = create_app(ProductionConfig)