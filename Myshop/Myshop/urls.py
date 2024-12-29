from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from shop.views import helloworld  # ایمپورت ویوی helloworld

urlpatterns = [
    path('admin/', admin.site.urls),
   # path('', helloworld, name='home'),  # مسیر اصلی برای صفحه اصلی
    path('', include('shop.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
