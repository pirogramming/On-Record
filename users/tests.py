from django.test import TestCase, Client
from django.contrib.auth import get_user_model, authenticate
from django.urls import reverse
from users.models import EmailVerification
import uuid
from datetime import timedelta
from django.utils.timezone import now

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
        self.client.login(email="test@example.com", password="password123")

    def test_user_creation(self):
        """User 모델이 정상적으로 생성되는지 테스트"""
        user = User.objects.create_user(email="newuser@example.com", nickname="newuser", password="password123")
        self.assertEqual(user.email, "newuser@example.com")
        self.assertEqual(user.nickname, "newuser")
        self.assertTrue(user.check_password("password123"))

    def test_main_view(self):
        """메인 페이지 렌더링 테스트"""
        response = self.client.get(reverse("users:main"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/main.html")

    def test_login(self):
        """일반 로그인 테스트"""
        login_data = {"username": "test@example.com", "password": "password123"}
        response = self.client.post(reverse("users:user_login"), login_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(authenticate(email="test@example.com", password="password123"))

    def test_logout(self):
        """로그아웃 테스트"""
        response = self.client.get(reverse("users:logout"))
        self.assertEqual(response.status_code, 302)

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