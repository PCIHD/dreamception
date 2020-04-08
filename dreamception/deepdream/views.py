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
Media_dir = os.path.join(BASE_DIR, 'deepdream/media/')


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
            print(self.request.POST)
            if(image.is_valid()):
                image.save()
            return JsonResponse({"status": 200}, status=200)

        return JsonResponse({"success": False}, status=400)


def handle_uploaded_file(f):
    print(f.name)
    with open(Media_dir + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

