from django.urls import path, include
from .import views

app_name = 'plr'

urlpatterns = [
    path('', views.post_list, name='player_list'),
    path('<slug:player>', views.PlayerDetailView.as_view(), name='player_detail'),
    path('search/', views.player_search, name='player_search'),
    path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount'))
]