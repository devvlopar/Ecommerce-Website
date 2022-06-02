from django.contrib import admin

from seller.models import *

# Register your models here.

admin.site.register(SellerUser)
#admin.site.register(Product)

@admin.register(Product)
class UserAdmin(admin.ModelAdmin):
    list_display=['name','des','price','quantity','pic','discount','seller']