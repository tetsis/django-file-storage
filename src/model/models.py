from django.db import models
from datetime import datetime

# Create your models here.

class GCP_File(models.Model):
    name = models.CharField(max_length=2048, default="")
    upload_time = models.DateTimeField(default=None, blank=True, null=True)
 
    def __str__(self):
        return self.name

class AWS_File(models.Model):
    name = models.CharField(max_length=2048, default="")
    upload_time = models.DateTimeField(default=None, blank=True, null=True)
 
    def __str__(self):
        return self.name

class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    caption = models.CharField(max_length=2048, default="")