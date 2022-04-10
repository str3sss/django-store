import uuid
from django.contrib.sessions.models import Session
from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    email = models.EmailField(unique=True,max_length=250)
    avatar = models.ImageField(null=True, default="avatar.svg")

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    seller =  models.ForeignKey(User,on_delete=models.CASCADE ,related_name='products')
    category = models.ForeignKey(Category, related_name='products',on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=200, db_index=True)
    image = models.ImageField(blank=True,null = True)
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name
    
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
    

class Order(models.Model):
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, blank=True, null=True)