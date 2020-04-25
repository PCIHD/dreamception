from django import forms
from .models import Photo, Dream_Config


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('title','fileUpload',)





class dream_settings(forms.ModelForm):
    class Meta:
        model = Dream_Config
        fields = ('octave','scale','layer')


class response(forms.Form):
    image = forms.ImageField()