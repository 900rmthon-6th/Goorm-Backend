from fastapi import APIRouter, Response
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from dotenv import load_dotenv

import json
import openai
import os

load_dotenv()

router = APIRouter()

mongo_client: MongoClient
database: Database
spot_collection: Collection

# Initialize the OpenAI ChatGPT model
openai.api_key = os.getenv("OPENAI_API_KEY")
model_name = "gpt-3.5-turbo"


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
    res_doc = {"data": spot_list}
    return res_doc


@router.get("/spot/{mbti}/chat")
def get_spot_chat(mbti: str, response: Response):
    connect_to_mongo()
    spots = spot_collection.find({"mbti": mbti})
    spot_list = []
    for spot in spots:
        spot_data = {
            "title": spot.get("title"),
            "tag": spot.get("tag"),
            "des": spot.get("des"),
        }
        spot_list.append(spot_data)

    spot_list_str = ", ".join(
        [
            f"Title: {spot['title']}, Tag: {spot['tag']}, Description: {spot['des']}"
            for spot in spot_list
        ]
    )

    pre_msg = "제주도 안의 워킹홀리데이 후보지 정보들이야 " + spot_list_str

    user_msg = "너는 대한민국에서 가장 뛰어난 문화기획자야. 대한민국에는 제주도라는 가장 자연친화적이고 아름다운 섬이 있어. 하지만 젊은 청년층이 부족하여서 이 곳의 농업, 수업 분야에서 일할 젊은 인력이 부족한 현실이야. 너는 젊은 청년층이 제주도에 여행하면서 일거리와 숙식을 제공하는 워킹홀리데이 서비스를 기획하고 있어. "
    user_msg += f"이번에 추천하고자하는 여행지들을 방문할 방문자의 MBTI는 {mbti}야. 이 여행자에게 적절한 장소를 추천해줘."

    # Send user message to ChatGPT and get the model's response
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": pre_msg,
            },
            {
                "role": "user",
                "content": user_msg,
            },
        ],
    )

    print(completion)
    completion_json = json.loads(str(completion))
    print(completion_json)

    chat_result = completion_json
    response.headers["Content-Type"] = "application/json"
    return chat_result
