from django.urls import path
from . import views


urlpatterns = [
    path('fotos/', views.FotoimovelListView.as_view(), name='fotos_list'),
    path('fotos/novo/', views.FotoimovelCreateView.as_view(), name='fotos_create'),
    path('fotos/<int:pk>/', views.FotoimovelDetailView.as_view(), name='fotos_detail'),
    path('fotos/<int:pk>/editar/', views.FotoimovelUpdateView.as_view(), name='fotos_update'),
    path('fotos/<int:pk>/excluir/', views.FotoimovelDeleteView.as_view(), name='fotos_delete'),
]
