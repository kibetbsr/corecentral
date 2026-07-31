from django.urls import path
from . import views

app_name = 'matches'

urlpatterns = [
    path('', views.FixturesListView.as_view(), name='fixtures'),
    path('<int:pk>/', views.MatchDetailView.as_view(), name='match_detail'),
]