from django.db import models

from users.models import User
from diaries.models import Diary,Pet

# Create your models here.


class Like(models.Model):
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE)
    like_user = models.ForeignKey(User, related_name="like_user", on_delete=models.CASCADE)


class Comment(models.Model):
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE , related_name='diary')
    comment_user = models.ForeignKey(User, related_name="comment_user", on_delete=models.CASCADE)
    content = models.TextField()


