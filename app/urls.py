
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('', include('Imoveis.urls')),
    path('', include('Bairros.urls')),
    path('', include('Cidades.urls')),
    path('', include('Corretores.urls')),
    path('', include('Fotos.urls')),

    path('api/v1/', include('Imoveis.api_urls')),
    path('api/v1/', include('Bairros.api_urls')),
    path('api/v1/', include('Cidades.api_urls')),
    path('api/v1/', include('Corretores.api_urls')),

    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
