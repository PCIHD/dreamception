from django.shortcuts import render

# Create your views here.
from django.views import View
from django.http import JsonResponse

import numpy as np


from .forms import PhotoForm,Dream_Config
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Media_dir = os.path.join(BASE_DIR, 'deepdream/media/photos')

name = ''
class IndexView(View):
    # print("VERIFICATION: ")
    template_name = 'index.html'
    def get(self, *args, **kwargs):

        return render(self.request, self.template_name, {}) 

    def post(self, *args, **kwargs):
        if (self.request.method == 'POST'):
            image = PhotoForm(self.request.POST, self.request.FILES)
            print(self.request.FILES)
            name = self.request.POST['title']

            if (image.is_valid()):
                image.save()


            return JsonResponse({"status": 200 }, status=200)

        return JsonResponse({"success": False}, status=400)


class Dream(View):
    template_name = 'deepdream.html'


    def get(self, *args, **kwargs):

        return render(self.request, self.template_name, {})

    def post(self, *args, **kwargs):


        if (self.request.method == 'POST'):







            return JsonResponse({"status": 200 } , status=200)

        return JsonResponse({"success": False}, status=400)

def download(img, max_dim=None):

    if max_dim:
        img.thumbnail((max_dim, max_dim))
    return np.array(img)

