from django.urls import path
from . import views


urlpatterns = [
    path('corretores/', views.CorretorListView.as_view(), name='corretores_list'),
    path('corretores/novo/', views.CorretorCreateView.as_view(), name='corretores_create'),
    path('corretores/<int:pk>/', views.CorretorDetailView.as_view(), name='corretores_detail'),
    path('corretores/<int:pk>/editar/', views.CorretorUpdateView.as_view(), name='corretores_update'),
    path('corretores/<int:pk>/excluir/', views.CorretorDeleteView.as_view(), name='corretores_delete'),
]
