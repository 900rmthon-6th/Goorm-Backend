import openai
import json

openai.api_key ="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"
completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo", 
  messages=[{"role": "user", "content": "나는 제주도민인데, 워킹홀리데이를 제주도로 오게 만들고 싶어, 적절한 워킹홀리데이가 가능한 제주도 스팟을 추천해줄래?"},
            {"role": "assistant", "content": "제주도는 한국의 아름다운 섬이야"}]
)

print(completion)
completion_json = json.loads(str(completion))
print(completion_json["choices"][0]["message"]["content"])
