from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

urlpatterns = [
    path('cidades/', login_required(views.CidadeListView.as_view()), name='cidades_list'),
    path('cidades/novo/', login_required(views.CidadeCreateView.as_view()), name='cidades_create'),
    path('cidades/<int:pk>/', login_required(views.CidadeDetailView.as_view()), name='cidades_detail'),
    path('cidades/<int:pk>/editar/', login_required(views.CidadeUpdateView.as_view()), name='cidades_update'),
    path('cidades/<int:pk>/excluir/', login_required(views.CidadeDeleteView.as_view()), name='cidades_delete'),
]
