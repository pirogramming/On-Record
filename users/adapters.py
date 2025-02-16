from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.utils import valid_email_or_none
from django.contrib.auth import get_user_model
from allauth.socialaccount.models import SocialAccount

User = get_user_model()

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # 소셜 로그인 시 기존 일반 로그인 이메일이 있으면 연결
        email = sociallogin.account.extra_data.get("email")

        if email:
            try:
                # 같은 이메일을 가진 기존 계정이 있는지 확인
                user = User.objects.get(email=email)

                # 기존 계정과 소셜 계정 연결
                sociallogin.connect(user)
                sociallogin.state['user'] = user

            except User.DoesNotExist:
                pass # 기존 계정이 없으면 새 계정을 생성


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