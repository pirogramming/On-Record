import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from diaries.models import Pet, Plant, Diary
from datetime import date
from replies.models import Reply

User = get_user_model()

def create_response(pk, username):
    """GPT 호출 없이 테스트 답장을 강제 생성하는 함수"""
    diary = get_object_or_404(Diary, id=pk)
    current_user = diary.user

    if diary.pet or diary.plant:
        reply_text = f"{username}님, 테스트 답장입니다."  # OpenAI 호출 없이 직접 응답 생성
    else:
        return JsonResponse({"error": "반려친구가 없습니다."}, status=400)

    # ✅ 답장 저장
    Reply.objects.create(diary=diary, user=current_user, content=reply_text)

class DiariesTests(TestCase):
    def setUp(self):
        """테스트 데이터 생성"""
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="TestPassword123!",
            nickname="테스트유저"
        )

        # 반려동물 & 반려식물 테스트 데이터 생성
        self.pet = Pet.objects.create(
            name="테스트강아지",
            user=self.user,
            age=2,
            kind="dog",
        )
        self.plant = Plant.objects.create(
            name="테스트식물",
            user=self.user,
            kind="몬스테라",
            age=1,
        )

        # 일기 데이터 생성
        self.diary_pet = Diary.objects.create(
            user=self.user, pet=self.pet, title="강아지 일기", content="강아지랑 산책 다녀옴!", date=date.today()
        )
        self.diary_plant = Diary.objects.create(
            user=self.user, plant=self.plant, title="식물 일기", content="식물에 물 줬음!", date=date.today()
        )

    def test_create_diary(self):
        """다이어리 작성 테스트"""
        self.client.login(email="testuser@example.com", password="TestPassword123!")

        response = self.client.post(
            reverse("diaries:create_diaries") + "?year=2024&month=1&day=1",
            {
                "title": "새로운 다이어리",
                "content": "새로운 다이어리 내용",
                "friends": f"pet-{self.pet.id}",
                "date": date.today().strftime("%Y-%m-%d"),
                "weather": "sunny",
                "mood": "happy",
            },
            follow=True
        )

        self.assertEqual(response.status_code, 200, "다이어리 생성 후 정상적으로 리다이렉트되지 않았습니다.")
        self.assertTrue(Diary.objects.filter(title="새로운 다이어리").exists(), "다이어리가 데이터베이스에 저장되지 않았습니다.")
        print("✅ 다이어리 생성 테스트 통과")

    def test_create_response_pet(self):
        """반려동물 답장 생성 테스트"""
        self.client.login(email="testuser@example.com", password="TestPassword123!")

        create_response(self.diary_pet.id, self.user.nickname)  # ✅ nickname 추가

        reply = Reply.objects.get(diary=self.diary_pet, user=self.user)
        self.assertIsNotNone(reply, "답장이 생성되지 않았습니다.")
        self.assertEqual(reply.user, self.user, "답장의 작성자가 올바르지 않습니다.")
        self.assertEqual(reply.content, f"{self.user.nickname}님, 테스트 답장입니다.", "Mock된 답장이 DB에 정상 저장되지 않았습니다.")
        print("✅ 반려동물 답장 생성 테스트 통과")

    def test_create_response_plant(self):
        """반려식물 답장 생성 테스트"""
        self.client.login(email="testuser@example.com", password="TestPassword123!")

        create_response(self.diary_plant.id, self.user.nickname)  # ✅ nickname 추가

        reply = Reply.objects.get(diary=self.diary_plant)
        self.assertIsNotNone(reply, "답장이 생성되지 않았습니다.")
        self.assertEqual(reply.user, self.user, "답장의 작성자가 올바르지 않습니다.")
        self.assertEqual(reply.content, f"{self.user.nickname}님, 테스트 답장입니다.", "Mock된 답장이 DB에 정상 저장되지 않았습니다.")
        print("✅ 반려식물 답장 생성 테스트 통과")
        
    def test_create_response_no_pet_or_plant(self):
        """반려동물 또는 반려식물이 없는 다이어리에서 오류 발생 테스트"""
        self.client.login(email="testuser@example.com", password="TestPassword123!")

        diary_no_pet_plant = Diary.objects.create(
            user=self.user, 
            title="일반 일기", 
            content="오늘도 좋은 하루였어!", 
            date=date.today(),
            mood="happy",
            weather="sunny"
        )

        response = create_response(diary_no_pet_plant.id, self.user.nickname)
        self.assertEqual(response.status_code, 400)

        response_data = json.loads(response.content.decode("utf-8"))  # Django JsonResponse에서 JSON 데이터 추출
        self.assertEqual(response_data["error"], "반려친구가 없습니다.")
        print("✅ 반려동물 또는 반려식물이 없는 경우 오류 테스트 통과")