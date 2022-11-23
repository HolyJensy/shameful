from django import forms
from main.models import Gallery, Photo

class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ['title']
        widjets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),

        }


class PhotoCreateForm(forms.ModelForm):
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gallery'].queryset = Gallery.objects.filter(user=user)

    class Meta:
        model = Photo
        fields = ['title', 'gallery', 'image']
        widjets = {
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'gallery':forms.Select(attrs={'class':'form-control'}),
            'image':forms.ImageField().widget
        }
