from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.


class pages_content(models.Model):
    name = models.CharField(max_length=50)
    content =  RichTextUploadingField()


    def __str__(self):
        return self.name
    