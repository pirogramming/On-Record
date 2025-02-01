from django import forms
from .models import Friend, Personality

# 반려동물 등록 폼
class FriendForm(forms.ModelForm):
    personal = forms.ModelMultipleChoiceField(
        queryset = Personality.objects.all(), # 성격 목록을 가져옴
        widget = forms.CheckboxSelectMultiple, # 체크 박스로 표시
        required = False
    )

    class Meta:
        model = Friend
        fields = ['name', 'kind', 'gender', 'age', 'personal', 'image']