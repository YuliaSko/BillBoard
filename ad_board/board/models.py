from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from . import extensions


class User(AbstractUser):
    """Модель пользователя, добавляем поле кода"""
    code = models.CharField(max_length=5, blank=True, null=True)


class Ad(models.Model):
    """Объявление, связь с моделью пользователя"""
    ad_user = models.ForeignKey(User, on_delete=models.CASCADE)

    category = models.CharField(max_length=2, choices=extensions.CATEGORY, default=None)
    title = models.CharField(max_length=255)
    text = RichTextUploadingField()
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title

    def preview(self):
        preview = self.text[:30]
        return preview

    def get_absolute_url(self):
        return reverse('ad_detail', args=[str(self.id)])

    def len_responses(self):
        return len(AdResponse.objects.filter(ad_response=self.pk))


class AdResponse(models.Model):
    """Отклик на объявление, связь с моделями пользователя и объявления"""
    user_response = models.ForeignKey(User, on_delete=models.CASCADE)
    ad_response = models.ForeignKey(Ad, on_delete=models.CASCADE)

    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.content[:50]}....'

    def get_absolute_url(self):
        return reverse('ad_detail', args=[str(self.id)])
