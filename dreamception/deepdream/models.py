from django.db import models

class Photo(models.Model):
    title = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
class Dream_Config(models.Model):

    octave = models.DecimalField(max_digits=2,decimal_places=1)
    iteration = models.IntegerField()
# Create your models here.
class Images(models.Model):
    title = models.CharField(max_length=50)
    file = models.FileField(upload_to='dreamception/media/')

    def __unicode__(self):
        return self.image.url

