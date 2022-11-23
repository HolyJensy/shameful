from django.contrib import admin
from .models import Advert, Photo, Gallery

@admin.register(Advert) # подключение нашей модели Advert к админке
class AdvertAdmin(admin.ModelAdmin):
    search_fields = ['title', 'text', 'email'] # Возможность поиска по описанию
    list_filter = ('user',) # Фильтр фоток


@admin.register(Photo) #Декоратор для регистрации модели в админке
class PhotoAdmin(admin.ModelAdmin):
    search_fields = ['title'] # Возможность поиска по описанию
    list_filter = ('gallery',) # Фильтр фоток

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    search_fields = ['title'] # Возможность поиска по описанию
    list_filter = ('user',)