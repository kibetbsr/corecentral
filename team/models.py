from django.db import models
from django.urls import reverse
from django.db.models import Case, When, Value, IntegerField


class PlayerManager(models.Manager):
    def get_queryset(self):
        position_order = Case(
            When(position='GK', then=Value(1)),
            When(position='DF', then=Value(2)),
            When(position='MF', then=Value(3)),
            When(position='FW', then=Value(4)),
            output_field=IntegerField(),
        )
        return super().get_queryset().annotate(
            position_priority=position_order
        ).order_by('position_priority', 'squad_number')


class Player(models.Model):
    POSITION_CHOICES = [
        ('GK', 'Goalkeeper'),
        ('DF', 'Defender'),
        ('MF', 'Midfielder'),
        ('FW', 'Forward'),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    squad_number = models.PositiveIntegerField(unique=True)
    position = models.CharField(max_length=2, choices=POSITION_CHOICES)
    nationality = models.CharField(max_length=50, default='Kenya')
    date_of_birth = models.DateField(null=True, blank=True)
    height_cm = models.PositiveIntegerField(null=True, blank=True, help_text='Height in centimetres')
    photo = models.ImageField(upload_to='players/', blank=True, null=True)
    bio = models.TextField(blank=True)

    appearances = models.PositiveIntegerField(default=0)
    goals = models.PositiveIntegerField(default=0)
    assists = models.PositiveIntegerField(default=0)
    clean_sheets = models.PositiveIntegerField(default=0, help_text='Relevant for goalkeepers/defenders')

    is_active = models.BooleanField(default=True)
    joined_date = models.DateField(null=True, blank=True)

    objects = PlayerManager()

    class Meta:
        ordering = ['position', 'squad_number']  # fallback; PlayerManager overrides actual queries

    def __str__(self):
        return f"#{self.squad_number} {self.first_name} {self.last_name} ({self.get_position_display()})"

    def get_absolute_url(self):
        return reverse('team:player_detail', args=[self.pk])

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Staff(models.Model):
    ROLE_CHOICES = [
        ('HC', 'Head Coach'),
        ('AC', 'Assistant Coach'),
        ('MGR', 'Team Manager'),
        ('KM', 'Kit manager'),
    ]

    full_name = models.CharField(max_length=100)
    role = models.CharField(max_length=4, choices=ROLE_CHOICES)
    photo = models.ImageField(upload_to='staff/', blank=True, null=True)
    bio = models.TextField(blank=True)

    class Meta:
        ordering = ['role', 'full_name']
        verbose_name_plural = 'Staff'

    def __str__(self):
        return f"{self.full_name} - {self.get_role_display()}"