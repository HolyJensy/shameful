from django import forms        #Библиотека Джанго, можно написать from django.forms import ModelForm и можно писать в классе class AdvertForm(ModelForm):
from .models import Advert, Gallery  # Указываем откуда наследуем .-из данной директории main, файл models.py

class AdvertForm(forms.ModelForm):

    def __init__(self, user=None, *args, **kwargs): #конструктор для галлереи
        super().__init__(*args, **kwargs)
        if user:
            pk = user
        else:
            pk = self.instance.user
        self.fields['gallery'].queryset = Gallery.objects.filter(user=pk)

    class Meta:
        model = Advert                               #наследуемая модель Advert
        fields = ['title', 'text', 'phone', 'email', 'gallery'] #Можно выбрать все посредством написания вместо [...] - '__all__'

        widgets = {                                  #Создание формы для панели редактирования
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'gallery': forms.Select(attrs={'class': 'form-control'}),
        }