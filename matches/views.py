from django.views.generic import TemplateView, DetailView

from .models import Match


class FixturesListView(TemplateView):
    template_name = 'base/fixtures.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['upcoming'] = Match.objects.filter(status='UPCOMING').order_by('match_date', 'kickoff_time')
        context['postponed'] = Match.objects.filter(status='POSTPONED').order_by('match_date')
        context['results'] = Match.objects.filter(status='COMPLETED').order_by('-match_date', '-kickoff_time').prefetch_related('scorers')
        context['next_match'] = context['upcoming'].first()
        return context


class MatchDetailView(DetailView):
    model = Match
    template_name = 'base/match_detail.html'
    context_object_name = 'match'