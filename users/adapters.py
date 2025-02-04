from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.utils import valid_email_or_none
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)

        # 이메일 저장
        email = valid_email_or_none(data.get("email"))

        # 이메일이 이미 존재하는지 확인
        if email:
            try:
                user = User.objects.get(email=email)  # 이메일로 기존 유저를 찾음
            except User.DoesNotExist:
                user.email = email  # 존재하지 않으면 새로 할당

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
        user.save()

        return user