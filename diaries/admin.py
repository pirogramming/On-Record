from django.contrib import admin
from .models import *

admin.site.register(Pet)
admin.site.register(Personality)
admin.site.register(Plant)
admin.site.register(Diary)
admin.site.register(Like)
admin.site.register(Comment)