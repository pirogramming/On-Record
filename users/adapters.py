from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.utils import valid_email_or_none
from django.contrib.auth import get_user_model
from allauth.socialaccount.models import SocialAccount
from django.shortcuts import redirect
from allauth.exceptions import ImmediateHttpResponse

User = get_user_model()

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # 소셜 로그인 시 기존 일반 로그인 이메일이 있으면 연결
        email = valid_email_or_none(sociallogin.account.extra_data.get("email"))
        provider = sociallogin.account.provider

        if not email:
            return

        try:
            user = User.objects.get(email=email)

            if not user.socialaccount_set.filter(provider=provider).exists():
                sociallogin.user = user
                sociallogin.save(request)

        except User.DoesNotExist:
            pass

    def save_user(self, request, sociallogin, form=None):
        # 기존 유저가 있으면 소셜 계정과 연결, 없으면 새 계정을 생성
        if sociallogin.user and sociallogin.user.is_authenticated:
            return sociallogin.user
        return super().save_user(request, sociallogin, form)


    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)

        # 이메일 저장
        user.email = valid_email_or_none(sociallogin.account.extra_data.get("email"))

        # 소셜 로그인 제공자에 따른 닉네임 설정
        if sociallogin.account.provider == 'naver':
            nickname = sociallogin.account.extra_data.get("name")
        elif sociallogin.account.provider == 'google':
            nickname = sociallogin.account.extra_data.get("name")
        else:
            nickname = None

        # 닉네임이 없거나 중복되면 자동 생성
        if not nickname or User.objects.filter(nickname=nickname).exists():
            base_nickname = nickname or "user"  # 닉네임이 없으면 기본값 "user" 사용
            count = 1
            new_nickname = base_nickname

            # 닉네임이 중복되면 숫자를 붙여가며 유니크한 닉네임 생성
            while User.objects.filter(nickname=new_nickname).exists():
                new_nickname = f"{base_nickname}_{count}"
                count += 1

            nickname = new_nickname

        user.nickname = nickname
        return user