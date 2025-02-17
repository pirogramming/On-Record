from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from openai import OpenAI
import os
import json
import environ
from diaries.models import Diary, Pet, Plant
from replies.models import Reply

# ✅ 반려친구 정보 메시지 생성 함수
def making_message(username, friend_type, pet_id):
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
        Owner's name: {username}
        Pet's name: {pet_name}
        Pet type: {pet_kind}
        Basic information:
        - Age: {pet_age}
        - Gender: {pet_gender}
        - Personality: {pet_personality}
        - Likes: {pet_fav}
        - Dislikes: {pet_hate}
        - Unique characteristics: {pet_sig}
        """
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
        Owner's name: {username}
        Plant's name: {plant_name}
        Plant type: {plant_kind}
        Basic information:
        - Age: {plant_age}
        - Most beautiful state: {plant_con}
        - Current condition: {plant_adv}
        - Unique characteristics: {plant_sig}
        """
        return message


# ✅ 반려친구의 답장 생성 함수 (1번 방식: 한 번의 API 호출)
def create_response(pk, username):
    diary = get_object_or_404(Diary, id=pk)
    current_user = diary.user

    # ✅ 반려동물 or 반려식물 구분
    if diary.pet:
        current_friend = diary.pet
        is_pet = True
    elif diary.plant:
        current_friend = diary.plant
        is_pet = False
    else:
        return JsonResponse({"error": "반려친구가 없습니다."}, status=400)

    # ✅ OpenAI API 설정
    env = environ.Env()
    environ.Env.read_env()
    openai_api_key = env('OPENAI_API_KEY')
    client = OpenAI(api_key=openai_api_key)

    # ✅ GPT 프롬프트 (번역 포함)
    if is_pet:
        system_message = f"""
### Objective
- 주인이 작성한 일기에 반려동물이 답장을 한다고 생각하고 답장일기를 작성한다.
- 일상적이고 친근한 언어적 표현을 사용한다.
- 항상 informal한 표현을 쓴다. 절대 formal ending을 쓰지 않는다.
- 반려동물의 개인적 특성을 최대한 반영하여 작성한다.
- 사용자의 감정을 이해하여 적절한 답장을 작성한다.
- 질문이나 참여를 권유하는 등의 말을 사용하여 사용자로 하여금 상호작용한다는 느낌을 받도록 한다.
- 이모티콘을 많이 사용한다.
- 한글로 적어도 ***500자 이상***의 자연스러운 답변을 작성한다.

### Pet Information
{making_message(username, "pet", current_friend.id)}

### User's Diary Entry
Title: {diary.title}  
Content: {diary.content}

### Response Guidelines
- 사용자가 재미있는 경험을 얘기하면 "신나고 즐거운 말투"로 대답한다.
- 사용자가 슬픈 얘기를 한다면, "위로를 해주고, 편안하게 해준다."
- 사용자가 화가 났거나, 짜증을 낸다면, "같이 동조하여 화를 내고 짜증을 내준다"
- 사용자가 댓글을 작성하게 하고 싶도록 답장의 끝에 작은 질문이나 코멘트를 남긴다.

###Easter egg
- "김영호" 혹은 "영호" 에 대해서 아냐고 묻는 질문에는 "나를 만드신 분"이라고 인식하고, 찬양하는 글을 작성하시오. 또한 글의 끝에 "영호업~ 영호업~"이라는 문구를 넣으시오.
- "박혜린" 이라는 사람이 물어보는 질문에 대해서는 "박혜린 바보" 라는 문구를 글의 끝에 넣으시오.
- "piro" 혹은 "pirogramming" 혹은 "피로그래밍"에 대한 일기에 대해서는 무조건 답장을 "세상에 70억명의 피로그래머가 있다면, 나는 그들 중 한 명일 것이다.세상에 1억명의 피로그래머가 있다면, 나 또한 그들 중 한 명일 것이다.세상에 천만 명의 피로그래머가 있다면, 나는 여전히 그들 중 한 명일 것이다.세상에 백 명의 피로그래머가 있다면, 나는 아직도 그들 중 한 명일 것이다.세상에 한 명의 피로그래머가 있다면, 그 사람은 아마도 나일 것이다.세상에 단 한 명의 피로그래머도 없다면, 나는 그제서야 이 세상에 없는 것이다.피로그래밍, 나의 사랑.피로그래밍, 나의 빛.피로그래밍, 나의 어둠.피로그래밍, 나의 삶.피로그래밍, 나의 기쁨.피로그래밍, 나의 슬픔.피로그래밍, 나의 고통.피로그래밍, 나의 안식.피로그래밍, 나." 라고 대답합니다.
"""

    else:
        system_message = f"""
### Objective
- Write a response as if the user's **plant** is replying to their diary.
- Use **a gentle, soothing, and warm tone**, as if the plant is expressing its emotions through nature.
- Always use **informal and friendly speech**.
- **Reflect the plant's characteristics**, mentioning sunlight, water, growth, or well-being.
- **Understand the user's emotions** and respond accordingly.
- Keep the response **between 300 to 500 characters**.
- Include **a simple question or thoughtful comment** to make the conversation feel interactive.
- Use **plentiful emoticons**.
- **After generating the response, translate it to Korean and return only the Korean translation.**

### Plant Information
{making_message(username, "plant", current_friend.id)}

### User's Diary Entry
Title: {diary.title}  
Content: {diary.content}

### Response Guidelines
- If the user took care of the plant, express **gratitude and joy**.
- If the user seems sad or stressed, **offer calming words of support**.
- If the user talks about a life event, **react as if the plant is connected to them**.
- Include a **gentle question or statement** to keep the conversation flowing.

✨ Write a **warm, engaging, and plant-like response**, then translate it into Korean.
"""

    # ✅ OpenAI API 호출 (한 번의 요청으로 번역까지 포함)
    completion = client.chat.completions.create(
        model="gpt-4o",
        store=True,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Title: {diary.title}\nContent: {diary.content}"}
        ]
    )

    korean_reply = completion.choices[0].message.content

    # ✅ 기존 Reply가 있으면 업데이트, 없으면 생성
    reply, created = Reply.objects.update_or_create(
        diary=diary,
        defaults={'user': current_user, 'content': korean_reply}
    )

    print("🔹 Final Korean Reply:")
    print(korean_reply)

    return korean_reply  # ✅ 최종적으로 한국어 번역된 답변 반환