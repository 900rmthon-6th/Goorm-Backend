from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class UserMBTIInput(BaseModel):
    uid: str
    ans: list[str]


@router.post("/user/mbti")
def create_user_mbti(user_data: UserMBTIInput):
    uid = user_data.uid
    ans = user_data.ans

    # Perform the necessary operations with the user data (e.g., store in the database)

    return {"message": f"User {uid} MBTI created successfully"}
