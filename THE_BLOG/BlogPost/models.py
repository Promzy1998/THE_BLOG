from django.conf import settings
from django.utils import timezone

# Create your models here.
from django.db import models
from PIL import Image
from django.core.exceptions import ValidationError
from django.utils.text import slugify

class DataPost(models.Model):
    CATEGORY_CHOICES = [
        ('tech', 'Tech'),
        ('fashion', 'Fashion'),
        ('lifestyle', 'Lifestyle'),
        ('health', 'Health'),
        ('bussiness', 'Bussiness'),
    ]
    PRIORITY_CHOICES = [
        ('BiggerPics', 'BiggerPics'),
        ('Normal', 'Normal'),
        ('FooterPics', 'FooterPics'),
    ]

    Title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True, max_length=100)

    PostImage = models.ImageField(upload_to='uploads/')
    buttonColor = models.CharField(max_length=7)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='tech')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Normal')
    Description = models.TextField(null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # Add created_at timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    # Add this field in your DataPost model
    nicknames = models.CharField(max_length=255, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.Title)
        super().save(*args, **kwargs) 
       

        if self.PostImage:
            img_path = self.PostImage.path
            img = Image.open(img_path)

            max_width = 600  # Resize target width

            # Only resize if width is larger than max
            if img.width > max_width:
                w_percent = max_width / float(img.width)
                h_size = int(float(img.height) * w_percent)
                img = img.resize((max_width, h_size), Image.LANCZOS)
                img.save(img_path)
              

    def __str__(self):
        return f"{self.Title} by {self.author.username}"
 