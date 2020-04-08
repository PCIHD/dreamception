from django import forms
from .models import Photo, Dream_Config, Images


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('file',)


class SettingsUpload(forms.ModelForm):
    class Meta:
        model = Dream_Config
        fields = ('octave', 'iteration')


class ImageUpload(forms.Form):

    file = forms.FileField()
