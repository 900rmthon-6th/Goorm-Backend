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
spot_collection: Collection


def connect_to_mongo():
    global mongo_client, database, spot_collection
    mongo_uri = os.getenv("MONGODB_URI")
    mongo_client = MongoClient(mongo_uri)
    database = mongo_client.get_database("snsn")
    spot_collection = database.get_collection("spot")


def close_mongo_connection():
    global mongo_client
    mongo_client.close()


@router.get("/spot")
def get_spot_count(response: Response):
    connect_to_mongo()
    spot_count = spot_collection.count_documents({})
    return spot_count


@router.get("/spot/{mbti}")
def get_spot(mbti: str, response: Response):
    connect_to_mongo()
    spots = spot_collection.find({"mbti": mbti})
    spot_list = []
    for spot in spots:
        spot_data = {
            "sid": spot.get("sid"),
            "title": spot.get("title"),
            "mbti": spot.get("mbti"),
            "tag": spot.get("tag"),
            "des": spot.get("des"),
            "loc": spot.get("loc"),
        }
        spot_list.append(spot_data)
    response.headers["Content-Type"] = "application/json"
    return spot_list
