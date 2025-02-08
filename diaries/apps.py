from django.apps import AppConfig


class DiariesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'diaries'

    # diaries/apps.py에서 signals.py를 import하여 실행되도록 설정
    def ready(self):
        import diaries.signals # signals.py 파일을 import하여 signals.py 파일의 내용이 실행되도록 함
