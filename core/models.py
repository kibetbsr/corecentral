from django.db import models


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"


class AchievementMilestone(models.Model):
    """Used for the club history / achievements timeline on The Club page."""
    year = models.PositiveIntegerField()
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['year']

    def __str__(self):
        return f"{self.year} - {self.title}"
