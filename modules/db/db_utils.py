from pymongo import MongoClient
from pymongo.database import Database
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

mongo_client: MongoClient
database: Database


def connect_to_mongo():
    global mongo_client, database
    mongo_uri = os.getenv("MONGODB_URI")
    mongo_client = MongoClient(mongo_uri)
    database = mongo_client.get_database()

def close_mongo_connection():
    global mongo_client
    mongo_client.close()

# Add functions for MongoDB CRUD operations


