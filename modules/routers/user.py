from collections import Counter
from fastapi import APIRouter, Response
from pydantic import BaseModel

import json
import logging
import openai
import re

router = APIRouter()


class UserMBTIInput(BaseModel):
    uid: str
    ans: list[str]


@router.post("/user/mbti")
def create_user_mbti(user_data: UserMBTIInput, response: Response):
    uid = user_data.uid
    ans = user_data.ans

    user_msg = "MBTI는 Myers-Briggs 유형 지표로써, 총 16가지의 성격유형이 존재해. 특정 사람을 인터뷰한 결과, 그는 여행을 할때 다음과 같은 행동을 선택한다고 답변했어. 이는 아래에 [주요 선택사항]이라는 이름으로 총 8가지의 답변을 전달해줄게. 이를 모두 읽어보고 핵심내용을 정리해서, 16가지 성격유형 중 하나로 선택해줘."
    user_msg += f"\n[주요 선택사항]\n{ans}"
    user_msg += "\nMBTI를 선택한 사유는 300자로 요약해줘"
    user_msg += "\n답변은 조금 재치있게 적어줘"
    user_msg += "\n아래의 답변 양식을 반드시 지켜줘"

    # the model's response
    user_msg += "\n[답변 양식]"
    user_msg += "\n1. MBTI 종류 :"
    user_msg += "\n2. MBTI를 선택한 사유 :"

    # Send user message to ChatGPT and get the model's response
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": user_msg,
            },
        ],
    )

    completion_json = json.loads(str(completion))
    print(completion_json)
    chat_content = completion_json["choices"][0]["message"]["content"]
    print(chat_content)

    chat_content_str = str(chat_content)
    mbti_matches = re.findall(r"([A-Z]{4})", chat_content_str)

    res_doc = {}
    if mbti_matches:
        mbti_counter = Counter(mbti_matches)
        mbti_counter['MBTI'] = 0
        print(mbti_counter)
        most_common_mbti = mbti_counter.most_common(1)[0][0]
        print("추출된 MBTI 유형:", most_common_mbti)
        res_doc["mbti"] = most_common_mbti
    else:
        print("MBTI 유형을 찾을 수 없습니다.")
        res_doc["mbti"] = "MBTI 유형을 찾을 수 없습니다."

    # MBTI를 선택한 사유
    res_doc["reason"] = chat_content_str

    chat_result = res_doc
    response.headers["Content-Type"] = "application/json"
    return chat_result
