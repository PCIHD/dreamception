from django.db import models

class Photo(models.Model):
    title = models.CharField(max_length=255, blank=True)
    fileUpload = models.ImageField(upload_to='photos/')
    dreamified = models.ImageField(upload_to='dreamified/')

class Dream_Config(models.Model):

    octave = models.DecimalField(max_digits=2,decimal_places=1)
    scale = models.DecimalField(max_digits=4 ,decimal_places=2)
    layer = models.IntegerField( default=42)
# Create your models here.

