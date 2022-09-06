from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
user_types=[(1,'user'),(2,'admin'),(3,'company')]

class CustomUser(AbstractUser):
    user_profile = models.OneToOneField('Profile', on_delete=models.CASCADE,null=True, blank=True)
    user_type = models.IntegerField(choices=user_types,null=True, blank=True)
 

class Profile(models.Model):
    name=models.CharField(max_length=100)
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    image=models.ImageField()
    email=models.EmailField()
    phone=models.CharField(max_length=50)
    created_at=models.DateTimeField(default=timezone.now)
    deleted_at=models.DateTimeField(default=timezone.now)
    user_type = models.IntegerField(choices=user_types, null=True, blank=True)
    
    def __str__(self):
        return self.user.username

class Category(models.Model):
    name=models.CharField(max_length=100,null=False)
    def __str__(self):
        return self.name
   
class Product(models.Model):
    name=models.CharField(max_length=100,null=False)
    category=models.ForeignKey(Category,on_delete=models.CASCADE) 
    description=models.TextField()
    slug = models.SlugField()
    image = models.ImageField()
    stock=models.IntegerField()
    def __str__(self):
        return self.name



class Product_Companies(models.Model):
    product_id=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='companies', null=True, blank=True)
    company_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True, blank=True)
    price=models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return '%s - %s' % (self.product_id.name, self.company_id)


class Cart(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product = models.ForeignKey(Product_Companies, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return  '%s - %s' % (self.product, self.user)

class Order_product(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True, blank=True)
    name=models.CharField(max_length=50)
    address=models.TextField()
    phone=models.CharField(max_length=50)
    product=models.ForeignKey(Product_Companies, on_delete=models.CASCADE,null=True, blank=True)
    ordered=models.BooleanField(default=False)
    def __str__(self):
        return  '%s - %s' % (self.product, self.user)

class Order(models.Model):
    order=models.ManyToManyField(Order_product)
    received=models.BooleanField(default=False)
    delivered=models.BooleanField(default=False)
