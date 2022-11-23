from django.contrib import admin
from .models import  Profile

@admin.register(Profile) #Декоратор для регистрации модели в админке
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'first_name', 'last_name'
    )