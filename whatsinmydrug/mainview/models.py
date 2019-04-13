from django.db import models

class PhotoModel(models.Model):
    photo = models.ImageField(upload_to = "photos", default="logo.png")
