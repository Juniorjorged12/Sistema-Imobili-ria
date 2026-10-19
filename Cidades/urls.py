from django.urls import path
from . import views

urlpatterns = [
    path('cidades/', views.CidadeListView.as_view(), name='cidades_list'),
    path('cidades/novo/', views.CidadeCreateView.as_view(), name='cidades_create'),
    path('cidades/<int:pk>/', views.CidadeDetailView.as_view(), name='cidades_detail'),
    path('cidades/<int:pk>/editar/', views.CidadeUpdateView.as_view(), name='cidades_update'),
    path('cidades/<int:pk>/excluir/', views.CidadeDeleteView.as_view(), name='cidades_delete'),
]
