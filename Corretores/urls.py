from django.urls import path
from . import views


urlpatterns = [
    path('corretores/', views.CorretorListCreateView.as_view(), name='corretor-list-create'),
    path('corretores/<int:pk>/', views.CorretorRetrieveUpdateDestroyView.as_view(), name='corretor-retrieve-update-destroy'),
]
