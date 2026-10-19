from django.urls import path
from . import views


urlpatterns = [
    path('bairros/', views.BairroListView.as_view(), name='bairros_list'),
    path('bairros/novo/', views.BairroCreateView.as_view(), name='bairros_create'),
    path('bairros/<int:pk>/', views.BairroDetailView.as_view(), name='bairros_detail'),
    path('bairros/<int:pk>/editar/', views.BairroUpdateView.as_view(), name='bairros_update'),
    path('bairros/<int:pk>/excluir/', views.BairroDeleteView.as_view(), name='bairros_delete'),
]