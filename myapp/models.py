from django.db import models

from seller.models import Product

# Create your models here.

class User(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=20)

    def __str__(self):
        return self.name



class Cart(models.Model):
    productid = models.ForeignKey(Product,on_delete=models.CASCADE)
    userid = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.userid)