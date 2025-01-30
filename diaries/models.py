from django.db import models
from users.models import User

class Diary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to="diary_images/%Y%m%d", blank=True, null=True)
    disclosure = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kind = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    personal = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="friend_images/%Y%m%d", blank=True, null=True)

    def __str__(self):
        return self.name


class Like(models.Model):
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE)
    diary_user = models.ForeignKey(User, related_name="diary_user", on_delete=models.CASCADE)
    friend = models.ForeignKey(Friend, on_delete=models.CASCADE)
    like_user = models.ForeignKey(User, related_name="like_user", on_delete=models.CASCADE)


class Comment(models.Model):
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE)
    diary_user = models.ForeignKey(User, related_name="comment_diary_user", on_delete=models.CASCADE)
    friend = models.ForeignKey(Friend, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, related_name="comment_user", on_delete=models.CASCADE)
    content = models.TextField()