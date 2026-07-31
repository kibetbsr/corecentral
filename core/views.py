from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import ContactForm
from .models import AchievementMilestone
from matches.models import Match
from news.models import NewsPost


class HomeView(TemplateView):
    template_name = 'base/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next_match'] = Match.objects.filter(status='UPCOMING').order_by('match_date', 'kickoff_time').first()
        context['latest_news'] = NewsPost.objects.filter(is_published=True).order_by('-publish_date')[:3]
        context['recent_result'] = Match.objects.filter(status='COMPLETED').order_by('-match_date').first()
        return context


class AboutView(TemplateView):
    template_name = 'base/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['milestones'] = AchievementMilestone.objects.all()
        return context


class ContactView(FormView):
    template_name = 'base/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('core:contact')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Thank you! Your message has been sent to Kipsolu Central FC. We'll be in touch soon.")
        return super().form_valid(form)
