from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views


urlpatterns = [
    path('corretores/', login_required(views.CorretorListView.as_view()), name='corretores_list'),
    path('corretores/novo/', login_required(views.CorretorCreateView.as_view()), name='corretores_create'),
    path('corretores/<int:pk>/', login_required(views.CorretorDetailView.as_view()), name='corretores_detail'),
    path('corretores/<int:pk>/editar/', login_required(views.CorretorUpdateView.as_view()), name='corretores_update'),
    path('corretores/<int:pk>/excluir/', login_required(views.CorretorDeleteView.as_view()), name='corretores_delete'),
]
