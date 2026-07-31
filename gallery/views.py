from django.views.generic import ListView
from .models import GalleryImage


class GalleryListView(ListView):
    model = GalleryImage
    template_name = 'base/gallery.html'
    context_object_name = 'images'
