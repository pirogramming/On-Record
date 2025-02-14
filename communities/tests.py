from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from communities.models import Like, Comment
from diaries.models import Diary, Pet
import json

User = get_user_model()


class CommunitiesTests(TestCase):
    def setUp(self):
        """테스트 데이터 생성"""
        self.client = Client()

        # 테스트 사용자 생성
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="TestPassword123!",
            nickname="테스트유저"
        )
        self.user2 = User.objects.create_user(
            email="another@example.com",
            password="TestPassword123!",
            nickname="다른유저"
        )

        # 반려동물 테스트 데이터 생성
        self.pet = Pet.objects.create(name="테스트강아지", user=self.user, age=2, kind="dog")

        # 일기 데이터 생성
        self.diary = Diary.objects.create(
            user=self.user, pet=self.pet, title="테스트 다이어리", content="테스트 일기 내용"
        )

    def test_render_communities_main(self):
        """커뮤니티 메인 페이지 렌더링 테스트"""
        response = self.client.get(reverse("communities:render_communities_main"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "communities/communities_main.html")

    def test_toggle_like(self):
        """좋아요 토글 테스트"""
        self.client.login(email="testuser@example.com", password="TestPassword123!")
        
        # 좋아요 추가 요청
        response = self.client.post(reverse("communities:toggle_like", args=[self.diary.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Like.objects.filter(diary=self.diary, like_user=self.user).count(), 1)

        # 좋아요 취소 요청
        response = self.client.post(reverse("communities:toggle_like", args=[self.diary.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Like.objects.filter(diary=self.diary, like_user=self.user).count(), 0)

    def test_add_comment(self):
        """댓글 추가 테스트"""
        self.client.login(email="testuser@example.com", password="TestPassword123!")

        comment_data = json.dumps({"comment": "테스트 댓글"})
        response = self.client.post(
            reverse("communities:add_comment", args=[self.diary.id]),
            data=comment_data,
            content_type="application/json"
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Comment.objects.filter(diary=self.diary, comment_user=self.user, content="테스트 댓글").exists())

    def test_delete_comment(self):
        """댓글 삭제 테스트"""
        self.client.login(email="testuser@example.com", password="TestPassword123!")

        # ✅ diary 필드에 Diary 객체를 할당하도록 수정
        comment = Comment.objects.create(
            diary=self.diary,  # ✅ Diary 객체를 사용해야 함
            comment_user=self.user,
            content="테스트 댓글"
        )

        response = self.client.post(reverse("communities:delete_comment", kwargs={"pk": comment.id}))

        self.assertEqual(response.status_code, 200, "댓글 삭제 후 응답이 200이 아닙니다.")

        with self.assertRaises(Comment.DoesNotExist):
            Comment.objects.get(id=comment.id)

        print("✅ 댓글 삭제 테스트 통과")
        
    def test_update_comment(self):
        """댓글 수정 테스트"""
        self.client.login(email="testuser@example.com", password="TestPassword123!")

        # 댓글 추가
        comment = Comment.objects.create(diary=self.diary, content="수정할 댓글", comment_user=self.user)

        # 댓글 수정 요청
        new_comment_data = json.dumps({"content": "수정된 댓글"})
        response = self.client.post(
            reverse("communities:update_comment", args=[comment.id]),
            data=new_comment_data,
            content_type="application/json"
        )
        
        self.assertEqual(response.status_code, 200)
        comment.refresh_from_db()
        self.assertEqual(comment.content, "수정된 댓글")