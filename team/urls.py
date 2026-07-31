from django.urls import path
from . import views

app_name = 'team'

urlpatterns = [
    path('', views.SquadListView.as_view(), name='squad'),
    path('player/<int:pk>/', views.PlayerDetailView.as_view(), name='player_detail'),
]
