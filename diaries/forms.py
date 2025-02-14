from django import forms
# from django.forms import ModelForm
from .models import Pet, Personality, Plant, Diary

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
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    disclosure = forms.BooleanField(
        required=False, widget=forms.HiddenInput()
    )

    # ✅ Pet과 Plant를 하나의 필드에서 선택하도록 커스텀 필드 생성
    friends = forms.ChoiceField(choices=[], required=True, label="누구에게 쓰실 건가요?")

    class Meta:
        model = Diary
        fields = ['title', 'weather', 'content', 'image', 'disclosure', 'date', 'mood', 'friends']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # ✅ 현재 사용자 가져오기
        print(user)
        super().__init__(*args, **kwargs)

        if user:
        # ✅ Pet과 Plant 데이터를 가져와서 choices에 추가
            pets = Pet.objects.filter(user=user)
            plants = Plant.objects.filter(user=user)

            pet_choices = [(f'pet-{p.id}', f'🐶 {p.name}') for p in pets]  # 동물 구분
            plant_choices = [(f'plant-{p.id}', f'🌿 {p.name}') for p in plants]  # 식물 구분

            # ✅ 최종적으로 하나의 choices 리스트로 결합
            self.fields['friends'].choices = [('none', '선택하세요')] + pet_choices + plant_choices