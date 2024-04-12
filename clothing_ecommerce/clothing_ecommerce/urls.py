
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from core.views import frontpage, men

urlpatterns = [
    path('', include('store.urls')),
    path('', frontpage, name='frontpage'),
    path('men/', men, name='men'),
    path('admin/', admin.site.urls),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
