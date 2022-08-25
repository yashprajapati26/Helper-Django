from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db.models import Q,Subquery,PositiveIntegerField
from django.utils.translation import gettext_lazy as _
from location_field.models.plain import PlainLocationField
# Create your models here.

USER_TYPE = (
    ("buyer", "buyer"),
    ("vendor", "vendor")
)

class SubqueryCount(Subquery):
    template = "(SELECT count(*) FROM (%(subquery)s) _count)"
    output_field = PositiveIntegerField()

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Please enter email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        print(password,"password")
        user = self.create_user(email, password=password,)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user



class VendorManager(models.Manager):
    def get_queryset(self):
        complexQuery = Q(user_type="vendor") & Q(is_active=True)
        return super().get_queryset().filter(complexQuery)


class User(AbstractUser):
    username = None
    password = models.CharField(_("password"), max_length=128, null=True, blank=True)
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=20,choices=USER_TYPE,default="buyer")
    mobileno = models.BigIntegerField(blank=True,null=True)
    state = models.CharField(max_length=100,blank=True,null=True)
    city = models.CharField(max_length=100,blank=True,null=True)
    profession = models.CharField(max_length=255,blank=True,null=True) 
    is_vendor_approved = models.BooleanField(default=False)


    objects = UserManager()
    vendors = VendorManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Vendor(User,VendorManager):

    vendors = VendorManager()

    class Meta:
        proxy = True


class OtpVerification(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    otp = models.CharField(max_length=10,null=True,blank=True)
    


class Service_category(models.Model):
    category_name = models.CharField(max_length=100)
    category_image = models.ImageField(default="cat.png",upload_to="    /")

    def __str__(self):
        return self.category_name

Status = (('Active','Active'),('Inactive','Inactive'))



class Custom_ServiceManager(models.Manager):
    def get_queryset(self):
        complexQuery = Q(is_approved=True) & Q(is_active=True)
        return super().get_queryset().filter(complexQuery)



class Service(models.Model):
    service_image = models.FileField(upload_to="service/",null=True,blank=True,default="default.png")
    category = models.ForeignKey(Service_category, related_name="service_cat", on_delete=models.CASCADE)
    service_name = models.CharField(max_length=100)
    price = models.FloatField()
    service_time = models.PositiveIntegerField(null=True,blank=True)
    description = models.TextField()
    city = models.CharField(max_length=255)
    location = PlainLocationField(based_fields=['city'], zoom=7)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    vendor = models.ForeignKey(User,on_delete=models.CASCADE)

    objects = models.Manager()
    activate = Custom_ServiceManager()
 
    def __str__(self):
        return self.service_name

from django.contrib.postgres.fields import ArrayField
from datetime import datetime
class Location(models.Model):
    name = models.CharField(max_length=180)
    data = ArrayField(models.TextField(max_length=256), blank=True)
    # location = PlainLocationField(based_fields=['city'], zoom=7)
    saved_at = models.DateTimeField(default=datetime.now)

    

    def __str__(self):
        return self.name
