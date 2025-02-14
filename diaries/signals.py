# Django의 signals를 활용해 서버가 실행될 때, Personality 테이블에 값이 없으면 기본 데이터를 넣어주는 기능을 구현
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Personality

@receiver(post_migrate)
def create_default_personalities(sender, **kwargs):
    """ 서버 실행 후 Personality 테이블이 비어 있으면 기본값을 추가 """
    if sender.name == 'diaries': # diaries는 Personality 모델이 속한 앱 이름
        default_personalities = [
            "상냥한", "다정한", "도도한", "활발한", "소심한", "겁많은", "사교적인", "고집센", "온순한", "예민한"
        ]
        for p in default_personalities:
            Personality.objects.get_or_create(type=p) # 중복 생성 방지
