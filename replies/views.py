from django.shortcuts import get_object_or_404, render

# 테스트용 코드
from django.http import HttpResponse, JsonResponse
from openai import OpenAI
import os
import json # json형식을 담기 위해 추가
import environ

from diaries.models import Diary , Pet , Plant
from replies.models import Reply


def making_message(username, friend_type , pet_id):
    username = username
    if friend_type == "pet":
        pet = Pet.objects.get(id=pet_id)
        pet_kind = pet.kind
        pet_name = pet.name
        pet_age = pet.age
        pet_gender = pet.gender
        pet_personality = ", ".join([p.type for p in pet.personal.all()])  
        pet_fav = pet.pet_fav
        pet_hate = pet.pet_hate
        pet_sig = pet.pet_sig

        message = f"""
        보호자의 이름 : {username}
        반려동물의 이름 : {pet_name}
        반려동물의 구분 : {pet_kind}
        반려동물의 기초정보
        - 나이 : {pet_age}
        - 성별 : {pet_gender}
        - 성격 : {pet_personality}
        - 좋아하는 것 : {pet_fav}
        - 싫어하는 것 : {pet_hate}
        - 구별되는 특징 : {pet_sig}
        """
        print(message)
        return message
    else:
        plant = Plant.objects.get(id=pet_id)
        plant_name = plant.name
        plant_kind = plant.kind
        plant_age = plant.age
        plant_adv = plant.plant_adv
        plant_con = plant.plant_con
        plant_sig = plant.plant_sig

        message = f"""
        보호자의 이름 : {username}
        반려식물의 이름 : {plant_name}
        반려식물의 구분 : {plant_kind}
        반려식물의 기초정보
        - 나이 : {plant_age}
        - 가장 사랑스러운 식물의 모습 : {plant_con}
        - 현재 관리상태 : {plant_adv}
        - 구별되는 특징 : {plant_sig}
        """
        print(message)
        return message

def create_response(pk , username):
    diary = get_object_or_404(Diary, id=pk)

    current_user = diary.user

    # ✅ 반려동물인지 반려식물인지 구분
    if diary.pet:
        current_friend = diary.pet
        is_pet = True
    elif diary.plant:
        current_friend = diary.plant
        is_pet = False
    else:
        return JsonResponse({"error": "반려친구가 없습니다."}, status=400)

    # ✅ 동물일 경우 personal 속성 사용, 식물일 경우 plant_adv 속성 사용
    if is_pet:
        system_message = f"""
        ###Objective
        사용자가 기르는 반려친구의 입장에서 사용자가 작성한 일기의 답장일기를 작성
        - 사용자에게 답장을 작성할때 '~했습니다.' 가 아닌 '~했어' 체로 대답함
        - 사용자를 부를때는 무조건 반말로 대답을 함
        - 답장일기의 형식은 100자 이상, 300자 내외의 대답임.
        - 동물의 특성을 최대한 살려서 대답할 것

        ##- 다음의 일기 내용을 보고 반려친구의 입장에서 위의 조건을 만족하도록 답장을 작성.
        """ + making_message(username,"pet", current_friend.id)
    else:
        system_message = f"""
        ###Objective
        사용자가 기르는 반려친구의 입장에서 사용자가 작성한 일기의 답장일기를 작성
        - 사용자에게 답장을 작성할때 '~했습니다.' 가 아닌 '~했어' 체로 대답함
        - 사용자를 부를때는 무조건 반말로 대답을 함
        - 답장일기의 형식은 100자 이상, 300자 내외의 대답임.
        - 식물의 특성을 최대한 살려서 대답할 것

        ##- 다음의 일기 내용을 보고 반려친구의 입장에서 위의 조건을 만족하도록 답장을 작성.
        """ + making_message(username,"plant", current_friend.id)

    # ✅ OpenAI API 설정
    env = environ.Env()
    environ.Env.read_env()
    openai_api_key = env('OPENAI_API_KEY')

    client = OpenAI(api_key=openai_api_key)

    # ✅ GPT 요청 데이터 설정 (식물과 동물에 따라 다르게 작성)
    
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