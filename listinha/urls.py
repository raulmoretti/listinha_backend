from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from backend import views
from backend.views.token import MyObtainTokenPairView

router = routers.DefaultRouter()

router.register(r'users', views.UserViewSet)
router.register(r'families', views.FamilyViewSet)
router.register(r'product', views.ProductViewSet)
router.register(r'cart', views.SMCartViewSet)
router.register(r'order', views.OrderViewSet)
router.register(r'request', views.FamilyRequestViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    # Autenticação
    path('token/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Endpoints da API
    path('api/', include(router.urls)),
    
    # OpenAPI 3
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

