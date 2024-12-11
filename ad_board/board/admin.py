from django.contrib import admin
from .models import *


class AdAdmin(admin.ModelAdmin):
    list_display = ('title',)


admin.site.register(Ad)
admin.site.register(User)
admin.site.register(AdResponse)
