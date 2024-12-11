from django_filters import (
    FilterSet, CharFilter, ModelChoiceFilter, DateFilter, ChoiceFilter
)
from .models import Ad, User, AdResponse
from . import extensions
from django.forms import DateInput


class AdUserFilter(FilterSet):
    category = ChoiceFilter(
        field_name='category',
        choices=extensions.CATEGORY,
        label='Категория',
    )

    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Название поста'
    )

    date = DateFilter(
        field_name='date',
        lookup_expr='gt',
        label='Публикации после',
        widget=DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Ad
        fields = {

            'category',
            'title',
            'date',
        }


class AdFilter(AdUserFilter):
    ad_user = ModelChoiceFilter(
        field_name='ad_user',
        queryset=User.objects.all(),
        label='Автор',
        empty_label='Все авторы'
    )

    class Meta:
        model = Ad
        fields = {
            'ad_user',
            'category',
            'title',
            'date',
        }


class ResponseUserFilter(FilterSet):
    ad_response = ModelChoiceFilter(
        field_name='ad_response',
        queryset=Ad.objects.all(),
        label='Объявление',
        empty_label='Все объявления'
    )

    date = DateFilter(
        field_name='date',
        lookup_expr='gt',
        label='Отклики после',
        widget=DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = AdResponse
        fields = {

            'ad_response',
            'date',
        }


class ResponseFilter(ResponseUserFilter):
    user_response = ModelChoiceFilter(
        field_name='user_response',
        queryset=User.objects.all(),
        label='Автор отклика',
        empty_label='Все авторы'
    )

    class Meta:
        model = AdResponse
        fields = {
            'user_response',
            'ad_response',
            'date',
        }
