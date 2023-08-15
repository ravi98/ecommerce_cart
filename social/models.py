from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
# Create your models here.

class CustomUM(BaseUserManager):
    def create_seller(self, *args, **kwargs):
        pan=kwargs.get('pan')
        gstin=kwargs.get('gstin')
        mobile_number=kwargs.get('mobile_number')
        
        if not (pan and gstin and mobile_number):
            raise ValueError("Missing Required fields")
        
        password=kwargs.pop('password')
        
        seller=self.model(**kwargs)
        seller.is_seller=True
        seller.set_password(password)
        seller.save(using=self._db)
        
        return seller
    
    def create_user(self, *args, **kwargs):
        password=kwargs.pop('password')
        
        user=self.model(**kwargs)
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, *args, **kwargs):
        superuser=self.create_user(*args, **kwargs)
        superuser.is_staff=True
        superuser.is_superuser=True
        superuser.save()


class CustomUser(AbstractUser):
    mobile_number=models.CharField(max_length=10, unique=True, null=False)
    is_seller=models.BooleanField(default=False)
    pan=models.CharField(max_length=10, null=True, unique=True, blank=True)
    gstin=models.CharField(max_length=15, null=True, unique=True, blank=True)
    slug=models.SlugField(max_length=255)
    
    objects=CustomUM()
    REQUIRED_FIELD=['username', 'mobile_number']
    
    def __str__(self) -> str:
        return self.email

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,
                            unique=True)
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("social:product_list_by_category", kwargs={"category_slug": self.slug})
       


class Product(models.Model):
    """
    Model containing the detail of product
    """
    
    name = models.CharField(max_length=100, null=False)
    slug = models.SlugField(max_length=255)
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE
                                 )
    image = models.ImageField(upload_to='products/%Y/%m/%d',
                                 blank=True)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    available = models.BooleanField(default=True)
    product_description = models.CharField(max_length=200, blank=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
            ]

    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse("social:product_detail", args=[self.id, self.slug])
    

class Address(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='address'
    )
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return f"{self.address},{self.city}-{self.postal_code}"


class Order(models.Model):
    delivery_choices=[
        ('Placed', 'Placed'),
        ('EnRoute', 'EnRoute'),
        ('Delivered', 'Delivered'),
    ]
    order_id=models.CharField(max_length=15, null=False)
    buyer=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name='buyer'
    )
    address=models.ForeignKey(
        Address,
        on_delete=models.DO_NOTHING
    )
    created=models.DateTimeField(auto_now_add=True)
    deliverd_date=models.DateTimeField(null=True)
    cancelled_date=models.DateTimeField(null=True)
    status=models.CharField(max_length=20, default="Placed", choices=delivery_choices)
    price=models.IntegerField(null=False)
    
    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]
    
    def __str__(self):
        return f'Order {self.id}'
    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItems(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    
    def get_cost(self):
        return self.price*self.quantity
    
    def __str__(self) -> str:
        return str(self.id)


class Inventory(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='product_seller',null=True , on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='product_inventory', on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(null=False)
    price = models.IntegerField(null=False)
    discounted_price = models.IntegerField(null=True)
    added_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self) -> str:
        return f"{self.product.name} {self.seller}"
