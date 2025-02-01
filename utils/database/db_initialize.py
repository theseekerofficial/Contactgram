from utils.processor.load_env import env_dict
from motor.motor_asyncio import AsyncIOMotorClient

mongo_uri = env_dict.get("MONGO_URI")

mongo_client = AsyncIOMotorClient(mongo_uri)
db = mongo_client.Contactgram
user_collection = db.users
