from django.contrib import admin
from .models import NewsPost


@admin.register(NewsPost)
class NewsPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'publish_date', 'is_published')
    list_filter = ('category', 'is_published')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish_date'
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'category', 'excerpt', 'content', 'featured_image')
        }),
        ('Publishing', {
            'fields': ('publish_date', 'is_published')
        }),
    )
