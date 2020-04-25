from django.shortcuts import render

# Create your views here.
from django.views import View
from django.http import JsonResponse,FileResponse
from datetime import datetime
import numpy as np
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.db.models.fields.files import ImageFieldFile
from .models import Photo
from .forms import PhotoForm
from .dream import dream
import os
from PIL import  Image
from django.core.files.base import ContentFile
from PIL import Image
from io import StringIO
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Media_dir = os.path.join(BASE_DIR, 'deepdream\media\photos')

name = ''  #the saved name will be called in the other function will work for only one user now



class IndexView(View):
    # print("VERIFICATION: ")
    template_name = 'index.html'
    def get(self, *args, **kwargs):

        return render(self.request, self.template_name, {}) 

    def post(self, *args, **kwargs):
        if (self.request.method == 'POST'):
            image = PhotoForm(self.request.POST, self.request.FILES)
            print(self.request.FILES)
            global name
            name = self.request.POST['title']

            print(name)

            if (image.is_valid()):

                image.save()


            return JsonResponse({"status": 200 }, status=200)

        return JsonResponse({"success": False}, status=400)


class Dream(View):
    template_name = 'deepdream.html'
    dreaming = dream()
    layer_dict = ['mixed0','mixed1','mixed2','mixed3','mixed4','mixed5','mixed6','mixed7','mixed8','mixed9','mixed10']


    def get(self, *args, **kwargs):
        image = Photo.objects.all().order_by("-id")[0]

        return render(self.request, self.template_name, {"img":image.fileUpload.url})

    def post(self, *args, **kwargs):
        print("inPost")


        if (self.request.method == 'POST'):


            image = Photo.objects.all().order_by("-id")[0]


            img = self.dreaming.download(image.fileUpload.path)

            print(self.request.POST , self.request.FILES)
            layer = int(self.request.POST['layerlist'])
            octave = []

            octave.append(int(self.request.POST['Octave1']))
            octave.append(int(self.request.POST['Octave2']))
            Scale = float(self.request.POST['Scale'])
            print(layer,octave,Scale)
            dreamified = self.dreaming.run_deep_dream_with_octaves(img ,octave_scale=Scale , octaves=range(octave[0],octave[1]) ,names = [self.layer_dict[layer]])
            img1 = np.array(dreamified)

            final = Image.fromarray(img1,'RGB')
            final.save(image.title)
            image.dreamified.save(image.title,open(image.title,'rb'))







            return JsonResponse({"success":True , "img":image.dreamified.url}, status=200 )

        return JsonResponse({"success": False}, status=400)



class ExtendedEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, ImageFieldFile):
            return str(o)
        else:
            return super().default(o)