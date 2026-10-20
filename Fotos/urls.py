from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views


urlpatterns = [
    path('fotos/', login_required(views.FotoimovelListView.as_view()), name='fotos_list'),
    path('fotos/novo/', login_required(views.FotoimovelCreateView.as_view()), name='fotos_create'),
    path('fotos/<int:pk>/', login_required(views.FotoimovelDetailView.as_view()), name='fotos_detail'),
    path('fotos/<int:pk>/editar/', login_required(views.FotoimovelUpdateView.as_view()), name='fotos_update'),
    path('fotos/<int:pk>/excluir/', login_required(views.FotoimovelDeleteView.as_view()), name='fotos_delete'),
]
