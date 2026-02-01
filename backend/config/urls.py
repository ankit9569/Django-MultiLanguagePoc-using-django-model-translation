from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.library.views import AuthorViewSet, BookViewSet

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'books', BookViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),  # Login/logout for browsable API
]