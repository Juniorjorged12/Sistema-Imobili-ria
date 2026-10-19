from django.urls import path
from . import views


urlpatterns = [
    path('imoveis/', views.ImovelListView.as_view(), name='imoveis_list'),
    path('imoveis/novo/', views.ImovelCreateView.as_view(), name='imoveis_create'),
    path('imoveis/<int:pk>/', views.ImovelDetailView.as_view(), name='imoveis_detail'),
    path('imoveis/<int:pk>/editar/', views.ImovelUpdateView.as_view(), name='imoveis_update'),
    path('imoveis/<int:pk>/excluir/', views.ImovelDeleteView.as_view(), name='imoveis_delete'),
]
