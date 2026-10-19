from django.urls import path

from . import views


urlpatterns = [
    path('cidades/', views.CidadeListCreateView.as_view(), name='cidade-list-create'),
    path(
        'cidades/<int:pk>/',
        views.CidadeRetrieveUpdateDestroyView.as_view(),
        name='cidade-retrieve-update-destroy',
    ),
]
