from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.utils import valid_email_or_none
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)

        # 이메일 저장
        user.email = valid_email_or_none(data.get("email"))

        # 구글 로그인인 경우 성과 이름을 결합하여 닉네임 생성 시도
        if sociallogin.account.provider == 'google':
            first_name = data.get("given_name") # 이름
            last_name = data.get("family_name") # 성
            nickname = f"{first_name} {last_name}" if first_name and last_name else first_name or last_name
        else:
            # 네이버 로그인인 경우
            nickname = data.get("name") or data.get("nickname")  # 닉네임 없으면 이름 사용 시도

        # 닉네임이 없거나 중복되면 자동 생성
        if not nickname or User.objects.filter(nickname=nickname).exists():
            base_nickname = f"user_{User.objects.count() + 1}"
            count = 1
            while User.objects.filter(nickname=base_nickname).exists():
                base_nickname = f"user_{User.objects.count() + 1}_{count}"
                count += 1
            nickname = base_nickname

        user.nickname = nickname
        return user