from fastapi import APIRouter
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter()

mongo_client: MongoClient
database: Database
mbti_collection: Collection


def connect_to_mongo():
    global mongo_client, database, mbti_collection
    mongo_uri = os.getenv("MONGODB_URI")
    print(mongo_uri)
    mongo_client = MongoClient(mongo_uri)
    database = mongo_client.get_database("snsn")
    mbti_collection = database.get_collection("mbti")


def close_mongo_connection():
    global mongo_client
    mongo_client.close()


@router.get("/mbti/{qid}")
def get_mbti(qid: str):
    connect_to_mongo()  # Ensure connection is established
    mbti_doc = mbti_collection.find_one({"qid": qid})
    if mbti_doc:
        return {"message": f"MBTI document found: {mbti_doc}"}
    else:
        return {"message": "MBTI document not found"}
