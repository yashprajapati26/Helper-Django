from django.db import models
from helper_app.models import User, Service
# Create your models here.


class Book_Service(models.Model):
    service = models.ForeignKey(Service,on_delete=models.CASCADE)
    customer = models.ForeignKey(User,on_delete=models.CASCADE)
    datetime = models.DateTimeField()   
    fullname = models.CharField(max_length=100)
    address = models.TextField(max_length=500)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=20)
    booked_at = models.DateTimeField(auto_now=True)

