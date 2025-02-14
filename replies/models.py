from django.db import models
from users.models import User
from diaries.models import Diary

class Reply(models.Model):
    diary = models.OneToOneField(Diary, on_delete=models.CASCADE , related_name="reply")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)