from pyexpat import model
from django.db import models

# Create your models here.

class SellerUser(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    password=models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Product(models.Model):
    name=models.CharField(max_length=100)
    des=models.TextField()
    price=models.FloatField()
    quantity=models.IntegerField()
    pic = models.FileField(upload_to='Product',null=True,blank=True)
    discount = models.IntegerField()
    seller = models.ForeignKey(SellerUser,on_delete=models.CASCADE)  # Foreignkey

    def __str__(self):
        return self.name