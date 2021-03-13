from io import BytesIO
from PIL import Image

from django.core.files import File
from django.db import models

from django.db import models
from apps.vendors.models import Vendor


class Category(models.Model):

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    ordering = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['ordering']


class Product(models.Model):

    def load_photo(self, file_name):
        file_type = file_name.split(".")[-1]
        file_name = ".".join(['{}/{}_{}', file_type])
        return file_name.format(
            self.category,
            self.title,
            self.date_added,
        )

    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to=load_photo, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_added']

    def get_tumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_tumbnail(self.image)
                self.save()
                return self.thumbnail.url
            else:
                return 'https://placeholder.com/240x180.jpg'

    def make_tumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)
        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        thumbnail = File(thumb_io, name=image.name)
        return thumbnail




