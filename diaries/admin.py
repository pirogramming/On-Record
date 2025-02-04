from django.contrib import admin
from .models import *

admin.site.register(Diary)
admin.site.register(Friend)
admin.site.register(Like)
admin.site.register(Comment)