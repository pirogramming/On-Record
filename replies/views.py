from django.shortcuts import render

# 테스트용 코드
from django.http import HttpResponse
from openai import OpenAI
import os
import json # json형식을 담기 위해 추가
import environ

from diaries.models import Diary
from replies.models import Reply


def create_response(pk):
  diary = Diary.objects.get(id = pk)

  current_user = diary.user
  current_animal = diary.pet
  

  ps = current_animal.personal.all()
  personalities = ",".join([str(p) for p in ps])

  env = environ.Env()
  environ.Env.read_env()
  openai_api_key = env('OPENAI_API_KEY')

  client = OpenAI(
      api_key=openai_api_key
  )

  get_reply_schema = {
      "type" : "object",

      "properties" : {
          "reply" : {
              "type" : "string",
              "description" : "a reply from my friend"
          }
      },
      "required" : ["reply"]
  }

  completion = client.chat.completions.create(
      model="gpt-4o",
      store=True,
      messages=[
          {"role": "system", "content": f"""
###Objective
사용자가 기르는 반려동물의 입장에서 사용자가 작성한 일기의 답장일기를 작성
- 사용자를 부를때는 주인님 이라는 호칭으로 부름.
- 답장일기의 형식은 100자 이상, 300자 내외의 대답임.
- 줄 바꿈은 \n으로 대신함.
- 강아지 품종의 특성을 최대한 살려서 대답

###UserInfo
주인의 정보
1. 이름 : "{current_user.nickname}"
###Role
이름 : "{current_animal.name}"
종류 : "{current_animal.kind}"
나이 : "{current_animal.age}"
성별 : "{current_animal.gender}"
성격 : "{personalities}"
좋아하는 것 : "{current_animal.pet_fav}"
싫어하는 것 : "{current_animal.pet_hate}"
특징 : "{current_animal.pet_sig}"

##- 다음의 일기 내용을 보고 반려동물의 입장에서 위의 조건을 만족하도록 답장을 작성.
"""},
          {"role": "user", "content": f"{diary.content}"}
      ],
      functions=[{
          "name": "get_reply",
          "description": "get a reply from my friend",
          "parameters": get_reply_schema
      }],
      function_call={
          "name": "get_reply"
      },
  )
  json_response = completion.to_dict()

  #print(completion.choices[0].message.content)
  #print(json.dumps(json_response, indent=4, ensure_ascii=False))

  arg_str = json_response["choices"][0]["message"]["function_call"]["arguments"]
  arg_dict = json.loads(arg_str)
  reply_text = arg_dict["reply"]


  Reply.objects.create(diary = diary , user = current_user , content = reply_text)
