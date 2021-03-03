from django.db import models

# Create your models here.
# Create class that represent our database

class Customer(models.Model):
    name = models.CharField(max_length=200, null=True) #null=true will let insert into table without filling out all the fields
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True) #Auto create/insert time whenever there is created instance in the Customer table

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=200, null=True) #null=true will let insert into table without filling out all the fields

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY = ( #tuple
        ('Indoor', 'Indoor'),
        ('Outdoor', 'Outdoor'),
    )
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    description = models.CharField(max_length=200, null=True, blank=True) #blank=True similar to null=True, but null=True is for form
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class Order(models.Model):

    STATUS = ( #tuple
        ('Pending', 'Pending'),
        ('Out of Delivery', 'Out of Delivery'),
        ('Delivered', 'Delivered'),
    )

    customer = models.ForeignKey(Customer,null=True, on_delete=models.SET_NULL) #whenever customer got delete, the order will remain in database with null value
    product = models.ForeignKey(Product,null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)

    def __str__(self):
        return self.product.name
    