from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views


urlpatterns = [
    path('bairros/', login_required(views.BairroListView.as_view()), name='bairros_list'),
    path('bairros/novo/', login_required(views.BairroCreateView.as_view()), name='bairros_create'),
    path('bairros/<int:pk>/', login_required(views.BairroDetailView.as_view()), name='bairros_detail'),
    path('bairros/<int:pk>/editar/', login_required(views.BairroUpdateView.as_view()), name='bairros_update'),
    path('bairros/<int:pk>/excluir/', login_required(views.BairroDeleteView.as_view()), name='bairros_delete'),
]