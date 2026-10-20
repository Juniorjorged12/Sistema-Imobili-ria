from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views


urlpatterns = [
    path('imoveis/', views.ImovelListView.as_view(), name='imoveis_list'),
    path(
        'imoveis/bairros-por-cidade/',
        login_required(views.bairros_por_cidade),
        name='bairros_por_cidade',
    ),
    path('imoveis/novo/', login_required(views.ImovelCreateView.as_view()), name='imoveis_create'),
    path('imoveis/<int:pk>/', views.ImovelDetailView.as_view(), name='imoveis_detail'),
    path('imoveis/<int:pk>/editar/', login_required(views.ImovelUpdateView.as_view()), name='imoveis_update'),
    path('imoveis/<int:pk>/excluir/', login_required(views.ImovelDeleteView.as_view()), name='imoveis_delete'),
]
