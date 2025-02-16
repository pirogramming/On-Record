from django.test import TestCase, Client
from django.contrib.auth import get_user_model, authenticate
from django.urls import reverse
from users.models import EmailVerification
from datetime import timedelta
from django.utils.timezone import now
from users.models import User
from diaries.models import Pet

User = get_user_model()

class UserTests(TestCase):
    def setUp(self):
        """테스트 유저 및 환경 설정"""
        self.client = Client()
        self.user = User.objects.create_user(
            email="test@example.com",
            nickname="testuser",
            password="password123"
        )
        login_success = self.client.login(email="test@example.com", password="password123")
        self.assertTrue(login_success, "로그인에 실패했습니다.")  # 로그인 성공 여부 체크

    def test_user_creation(self):
        """User 모델이 정상적으로 생성되는지 테스트"""
        user = User.objects.create_user(email="newuser@example.com", nickname="newuser", password="password123")
        self.assertEqual(user.email, "newuser@example.com")
        self.assertEqual(user.nickname, "newuser")
        self.assertTrue(user.check_password("password123"))

    def test_main_view(self):
        """메인 페이지 렌더링 테스트"""
        # Pet 객체 생성 시 필요한 필드 값 추가
        Pet.objects.create(
            user=self.user,
            name="Test Pet",
            age=2,  # NOT NULL 필드이므로 기본값 설정
            kind="dog",
            gender="male",
            pet_fav="공놀이",
            pet_hate="목욕",
            pet_sig="귀엽다"
        )

        # 로그인한 상태에서 메인 페이지 요청
        response = self.client.get(reverse("users:main"))

        # 메인 페이지가 diaries:view_calendar로 리다이렉트되었는지 확인
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("diaries:view_calendar"))

    def test_login(self):
        """일반 로그인 테스트"""
        login_data = {"email": "test@example.com", "password": "password123"}
        response = self.client.post(reverse("users:user_login"), login_data, follow=True)

        # 응답 상태 코드 확인 (200인지 302인지 체크)
        self.assertIn(response.status_code, [200, 302], f"Unexpected response status: {response.status_code}")

        # 로그인 후 세션 확인
        user_authenticated = self.client.session.get("_auth_user_id")
        self.assertIsNotNone(user_authenticated, "로그인 후에도 세션이 설정되지 않음")

        # 인증 확인
        user = authenticate(email="test@example.com", password="password123")
        self.assertIsNotNone(user, "authenticate()가 None을 반환함 (인증 실패)")

    def test_logout(self):
        """로그아웃 테스트"""
        response = self.client.get(reverse("users:logout"))
        self.assertEqual(response.status_code, 302)  # 로그아웃 후 리다이렉트

        # 세션이 제거되었는지 확인
        user_authenticated = self.client.session.get("_auth_user_id")
        self.assertIsNone(user_authenticated, "로그아웃 후에도 사용자가 남아 있음")

    def test_update_profile(self):
        """프로필 수정 테스트"""
        update_data = {"nickname": "updateduser"}
        response = self.client.post(reverse("users:update_profile"), update_data)
        self.user.refresh_from_db()
        self.assertEqual(self.user.nickname, "updateduser")

    def test_delete_user(self):
        """회원 탈퇴 테스트"""
        response = self.client.post(reverse("users:delete_user"))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(email="test@example.com").exists())

    def test_privacy_policy_view(self):
        """개인정보처리방침 페이지 테스트"""
        response = self.client.get(reverse("users:privacy_policy"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "privacy_policy.html")

    def test_terms_of_service_view(self):
        """이용약관 페이지 테스트"""
        response = self.client.get(reverse("users:terms_of_service"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "terms_of_service.html")