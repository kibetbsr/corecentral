from django.contrib import admin
from .models import ContactMessage, AchievementMilestone


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'submitted_at', 'is_read')
    list_filter = ('is_read', 'submitted_at')
    search_fields = ('name', 'email', 'subject', 'message')
    list_editable = ('is_read',)
    readonly_fields = ('submitted_at',)


@admin.register(AchievementMilestone)
class AchievementMilestoneAdmin(admin.ModelAdmin):
    list_display = ('year', 'title')
    list_filter = ('year',)
    search_fields = ('title', 'description')
    ordering = ('year',)
