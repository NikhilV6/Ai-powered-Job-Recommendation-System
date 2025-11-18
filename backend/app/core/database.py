from pymongo import MongoClient
from app.core.config import settings


client = MongoClient(settings.MONGO_URI)

# You can change DB name if you like
db = client["job_recommender"]
