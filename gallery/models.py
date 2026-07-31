from django.db import models
from django.db.models.functions import Coalesce
from django.db.models import F


class GalleryImage(models.Model):
    CATEGORY_CHOICES = [
        ('MATCHDAY', 'Matchday'),
        ('TRAINING', 'Training'),
        ('FANS', 'Fans & Community'),
        ('CLUB', 'Club Events'),
    ]

    title = models.CharField(max_length=150)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='MATCHDAY')
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=250, blank=True)
    taken_at = models.DateField(blank=True, null=True, help_text="Date the photo was taken (optional)")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-taken_at', '-uploaded_at']

    def __str__(self):
        return self.title
