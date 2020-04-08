from django.shortcuts import render

# Create your views here.
from django.views import View
from django.http import JsonResponse, HttpResponse

from django.urls import reverse
from .models import Photo
from .forms import PhotoForm, ImageUpload
from django.core.files.uploadedfile import SimpleUploadedFile
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Media_dir = os.path.join(BASE_DIR, 'deepdream\media')


class IndexView(View):
    # print("VERIFICATION: ")
    template_name = 'index.html'

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name, {})


class Dream(View):
    template_name = 'deepdream.html'


    def get(self, *args, **kwargs):

        return render(self.request, self.template_name, {})

    def post(self, *args, **kwargs):

        if (self.request.method == 'POST'):
            image = PhotoForm(self.request.POST, self.request.FILES)
            print(self.request.FILES)
            if(image.is_valid()):
                image.save()
            return JsonResponse({"success": self.request.POST}, status=200)
        else :

            return JsonResponse({"success": False}, status=400)



