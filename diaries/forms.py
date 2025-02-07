from django import forms
# from django.forms import ModelForm
from .models import Diary, Pet, Personality, Plant

# 반려동물 등록 폼
class PetForm(forms.ModelForm):
    personal = forms.ModelMultipleChoiceField(
        queryset = Personality.objects.all(), # 성격 목록을 가져옴
        widget = forms.CheckboxSelectMultiple, # 체크 박스로 표시
        required = False
    )

    class Meta:
        model = Pet
        fields = ['name', 'kind', 'gender', 'age', 'personal', 'image', 'pet_fav', 'pet_hate', 'pet_sig']
        widgets = {
            'pet_fav': forms.TextInput(attrs={'placeholder': '당근 간식을 가장 좋아해요'}),
            'pet_hate': forms.TextInput(attrs={'placeholder': '낯선 사람을 정말 싫어해요'}),
            'pet_sig': forms.TextInput(attrs={'placeholder': '눈이 정말 똘망똘망해요'}),
        }

class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ['kind', 'name', 'age', 'image', 'plant_con', 'plant_sig', 'plant_adv']
        widgets = {
            'age': forms.NumberInput(attrs={'placeholder': '개월 수를 입력하세요'}),
            'plant_con': forms.TextInput(attrs={'placeholder': '요즘 이파리가 시들시들해요'}),
            'plant_sig': forms.TextInput(attrs={'placeholder': '꽃 향기가 좋아요'}),
            'plant_adv': forms.TextInput(attrs={'placeholder': '한결같이 우리집 베란다에 있는 모습'}),
        }
    
class DiaryForm(forms.ModelForm):
    date = forms.DateField(
        widget = forms.DateInput(attrs = {'type': 'date'})
    )

    class Meta:
        model = Diary
        fields = ['title', 'weather', 'content', 'pet','image', 'disclosure', 'date', 'mood']