from django import forms

from .models import Ad, AdResponse


class AdCreateForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = [
            'title',
            'text',
            'category',
        ]
        labels = {
            'title': 'Заголовок объявления',
            'text': 'Текст объявления',
            'category': 'Категория объявления',
        }


class ResponseCreateForm(forms.ModelForm):
    class Meta:
        model = AdResponse
        fields = ['content',]
        labels = {
            'content': 'Текст отклика',
        }
