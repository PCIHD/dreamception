from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView


class IndexView(TemplateView):
    #print("VERIFICATION: ")
    template_name = 'index.html'