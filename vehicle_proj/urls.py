from django.contrib import admin
from django.urls import path
from django.views.decorators.cache import cache_page
from vehicle_app import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('brands-list/', views.BrandNameAPIView.as_view(), name='brands-list'),
    path('brands-list/<str:page_id>/', views.BrandNameAPIView.as_view(), name='brand-detail'),

    path('cars-list/', cache_page(60)(views.CarListAPIView.as_view()), name='car_list'),
    path('external-cars-list/', views.ExternalVehicleListAPIView.as_view(), name='car_list'),

    path('api/auth/register/', views.RegisterView.as_view(), name='auth_register'),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


]
