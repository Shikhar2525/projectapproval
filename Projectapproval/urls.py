from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from . import views
from django.conf.urls.static import static
urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('eproject/', include('eproject.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
