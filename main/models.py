import uuid
from django.db import models


class Product(models.Model):
    CATEGORIES = [
        ('FW', 'Footwear'),
        ('Sh', 'Shirts'),
        ('misc', 'Misc'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    price = models.IntegerField(default=0)
    description = models.TextField(max_length=1000)
    thumbnail = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORIES, default='FW')
    is_featured = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name

