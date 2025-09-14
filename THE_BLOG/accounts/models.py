from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify

class CustomUser(AbstractUser):
    """Custom user model extending AbstractUser."""
    username = models.CharField(max_length=100, blank=False, unique=True) 
    phone = models.CharField(max_length=20, unique=True)
    slugs = models.SlugField(unique=True,blank=True)
    def save(self, *args, **kwargs):
       if not self.slugs:
       # Slugify full name or username
         full_name =  self.username
         self.slugs = slugify(full_name)
         super().save(*args, **kwargs)
   
    
    
    def __str__(self):
        return self.username




