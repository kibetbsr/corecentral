from django.contrib import admin
from .models import Player, Staff


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('squad_number', 'first_name', 'last_name', 'position', 'nationality', 'appearances', 'goals', 'is_active')
    list_filter = ('position', 'is_active', 'nationality')
    search_fields = ('first_name', 'last_name')
    list_editable = ('is_active',)
    ordering = ('position', 'squad_number')
    fieldsets = (
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'squad_number', 'position', 'nationality', 'date_of_birth', 'height_cm', 'photo', 'bio')
        }),
        ('Stats', {
            'fields': ('appearances', 'goals', 'assists', 'clean_sheets')
        }),
        ('Status', {
            'fields': ('is_active', 'joined_date')
        }),
    )


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'role')
    list_filter = ('role',)
    search_fields = ('full_name',)
