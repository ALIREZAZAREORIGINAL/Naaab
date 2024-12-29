from django.db import models
import datetime


class Category(models.Model):
    name = models.CharField(max_length=30)
    picture = models.ImageField(upload_to='category_pictures/', default='path/to/default/image.jpg')



    def __str__(self):
        return self.name
    

class Brand(models.Model):
    Brandname = models.CharField(max_length=30)

    def __str__(self):
        return self.Brandname

class Customers(models.Model):
    FirstName = models.CharField(max_length=30)
    LasttName = models.CharField(max_length=30)
    PhoneNumber = models.CharField(max_length=13)
    Email = models.EmailField(max_length=100)
    Password = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.FirstName}{self.LasttName}'
    

class Prodocts(models.Model):
    Name = models.CharField(max_length=40)
    Description = models.CharField(max_length=200 , default='' , blank=True,null=True)
    Price = models.DecimalField(default=0 , decimal_places=0 , max_digits=12)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,default=1)
    Picture = models.ImageField(upload_to='upload/product')
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE,default=1)
    QuantityInStock = models.IntegerField(default=0)

    def __str__(self):
        return self.Name
    
class Orders (models.Model):
    product = models.ForeignKey(Prodocts , on_delete=models.CASCADE)
    customers = models.ForeignKey(Customers , on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=20 , default='', blank=False)
    phone = models.CharField(max_length=13 , blank=False)
    OrderDate = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.product}{self.customers}{self.address}{self.OrderDate}{self.status}'
    