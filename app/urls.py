
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/', include('Imoveis.urls')),
    path('api/v1/', include('Bairros.urls')),
    path('api/v1/', include('Corretores.urls')),
    path('api/v1/', include('Cidades.urls')),
]
