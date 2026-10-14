from django.urls import path
from . import views


urlpatterns = [
    path('bairros/', views.BairroListCreateView.as_view(), name='bairro-list-create'),
    path('bairros/<int:pk>/', views.BairroRetrieveUpdateDestroyView.as_view(), name='bairro-retrieve-update-destroy'),
]