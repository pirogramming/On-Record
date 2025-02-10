from django.shortcuts import get_object_or_404, render

# 테스트용 코드
from django.http import HttpResponse, JsonResponse
from openai import OpenAI
import os
import json # json형식을 담기 위해 추가
import environ

from diaries.models import Diary
from replies.models import Reply


def create_response(pk):
    diary = get_object_or_404(Diary, id=pk)

    current_user = diary.user

    # ✅ 반려동물인지 반려식물인지 구분
    if diary.pet:
        current_animal = diary.pet
        is_pet = True
    elif diary.plant:
        current_animal = diary.plant
        is_pet = False
    else:
        return JsonResponse({"error": "반려친구가 없습니다."}, status=400)

    # ✅ 동물일 경우 personal 속성 사용, 식물일 경우 plant_adv 속성 사용
    if is_pet:
        personalities = ",".join([str(p) for p in current_animal.personal.all()])
    else:
        personalities = f"식물 관리 팁: {current_animal.plant_adv}"  # 식물의 관리 팁 사용

    # ✅ OpenAI API 설정
    env = environ.Env()
    environ.Env.read_env()
    openai_api_key = env('OPENAI_API_KEY')

    client = OpenAI(api_key=openai_api_key)

    # ✅ GPT 요청 데이터 설정 (식물과 동물에 따라 다르게 작성)
    system_message = f"""
###Objective
사용자가 기르는 반려친구의 입장에서 사용자가 작성한 일기의 답장일기를 작성
- 사용자를 부를때는 주인님 이라는 호칭으로 부름.
- 답장일기의 형식은 100자 이상, 300자 내외의 대답임.
- 줄 바꿈은 \n으로 대신함.
- { '동물의 특성을 최대한 살려서 대답' if is_pet else '식물의 성장과 관련된 답장을 작성' }

##- 다음의 일기 내용을 보고 반려친구의 입장에서 위의 조건을 만족하도록 답장을 작성.
"""

    completion = client.chat.completions.create(
        model="gpt-4o",
        store=True,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"{diary.content}"}
        ],
        functions=[{
            "name": "get_reply",
            "description": "get a reply from my friend",
            "parameters": {
                "type": "object",
                "properties": {
                    "reply": {
                        "type": "string",
                        "description": "a reply from my friend"
                    }
                },
                "required": ["reply"]
            }
        }],
        function_call={"name": "get_reply"},
    )

    json_response = completion.to_dict()

    arg_str = json_response["choices"][0]["message"]["function_call"]["arguments"]
    arg_dict = json.loads(arg_str)
    reply_text = arg_dict["reply"]

    # ✅ 답장 저장
    Reply.objects.create(diary=diary, user=current_user, content=reply_text)