from fastapi import APIRouter, Response
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
    mongo_client = MongoClient(mongo_uri)
    database = mongo_client.get_database("snsn")
    mbti_collection = database.get_collection("mbti")


def close_mongo_connection():
    global mongo_client
    mongo_client.close()


@router.get("/mbti")
def get_mbti_count(response: Response):
    connect_to_mongo()
    mbti_count = mbti_collection.count_documents({})
    return mbti_count


@router.get("/mbti/{qid}")
def get_mbti(qid: str, response: Response):
    connect_to_mongo()  # Ensure connection is established
    mbti_doc = mbti_collection.find_one({"qid": qid})
    if mbti_doc:
        filtered_doc = {
            "qid": mbti_doc.get("qid"),
            "que": mbti_doc.get("que"),
            "ans": mbti_doc.get("ans"),
        }
        response.headers["Content-Type"] = "application/json"
        return filtered_doc
    else:
        response.status_code = 404
        return {"message": "MBTI document not found"}
