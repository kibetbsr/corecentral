from django.views.generic import ListView, DetailView
from .models import Player, Staff


class SquadListView(ListView):
    model = Player
    template_name = 'base/squad.html'
    context_object_name = 'players'
    queryset = Player.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        players = self.get_queryset()
        context['goalkeepers'] = players.filter(position='GK')
        context['defenders'] = players.filter(position='DF')
        context['midfielders'] = players.filter(position='MF')
        context['forwards'] = players.filter(position='FW')
        context['staff'] = Staff.objects.all()
        return context


class PlayerDetailView(DetailView):
    model = Player
    template_name = 'base/player_detail.html'
    context_object_name = 'player'
