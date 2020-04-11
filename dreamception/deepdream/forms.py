from django import forms
from .models import Photo, Dream_Config, Images


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('title','fileUpload',)




class ImageUpload(forms.ModelForm):
    class Meta:
        model = Images
        fields = ('title','fileUpload')


class dream_settings(forms.ModelForm):
    class Meta:
        model = Dream_Config
        fields = ('octave','scale','layer')