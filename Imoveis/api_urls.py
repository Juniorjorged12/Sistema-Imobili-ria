from django.urls import path

from . import views


urlpatterns = [
    path('imoveis/', views.ImovelListCreateView.as_view(), name='imovel-list-create'),
    path(
        'imoveis/<int:pk>/',
        views.ImovelRetrieveUpdateDestroyView.as_view(),
        name='imovel-retrieve-update-destroy',
    ),
]
