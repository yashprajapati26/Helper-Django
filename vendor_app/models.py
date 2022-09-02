from django.db import models
from helper_app.models import User, Service
# Create your models here.


class Book_Service(models.Model):
    customer = models.ForeignKey(User,on_delete=models.CASCADE)
    service = models.ForeignKey(Service,on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    address = models.TextField(max_length=500)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=20)
    booked_at = models.DateTimeField(auto_now=True)
