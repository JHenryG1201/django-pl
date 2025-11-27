from django.urls import path
from . import views

app_name = 'premier_league'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('team', views.TeamPageView.as_view(), name='team'),
    path('team/<int:pk>', views.TeamDetailPageView.as_view(), name='team-detail'),
    path('player', views.PlayerPageView.as_view(), name='player'),
    path('player/<int:pk>', views.PlayerDetailPageView.as_view(), name='player-detail'),
    path('fixture', views.FixturePageView.as_view(), name='fixture'),
    path('contact', views.ContactPageView.as_view(), name='contact',),
    path('fixture/<int:pk>', views.FixtureDetailPageView.as_view(), name='fixture-detail',),
]
