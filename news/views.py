from django.views.generic import ListView, DetailView
from .models import NewsPost


class NewsListView(ListView):
    model = NewsPost
    template_name = 'base/news_list.html'
    context_object_name = 'posts'
    paginate_by = 6
    queryset = NewsPost.objects.filter(is_published=True)


class NewsDetailView(DetailView):
    model = NewsPost
    template_name = 'base/news_detail.html'
    context_object_name = 'post'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return NewsPost.objects.filter(is_published=True)
