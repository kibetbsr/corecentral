from django.db import models
from django.urls import reverse
from django.utils import timezone


class NewsPost(models.Model):
    CATEGORY_CHOICES = [
        ('MATCH', 'Match Report'),
        ('CLUB', 'Club News'),
        ('TRANSFER', 'Transfers'),
        ('COMMUNITY', 'Community'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, help_text='URL-friendly version of the title')
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='CLUB')
    excerpt = models.CharField(max_length=300, blank=True, help_text='Short summary shown on listing pages')
    content = models.TextField()
    featured_image = models.ImageField(upload_to='news/', blank=True, null=True)
    publish_date = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-publish_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:post_detail', args=[self.slug])
