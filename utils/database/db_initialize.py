from pymongo import AsyncMongoClient
from utils.processor.load_env import env_dict

mongo_uri = env_dict.get("MONGO_URI")

mongo_client = AsyncMongoClient(mongo_uri)

db = mongo_client.Contactgram
chat_storage = mongo_client.ChatStorage
user_collection = db.users