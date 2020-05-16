from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from .views import (
    index,
    signinView,
    signupView
    )
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path(r'^tinymce/', include('tinymce.urls')),
    path('post/', include('post.urls')),
    path('signin/',signinView,name='signin'),
    path('signup/',signupView,name='signup'),
    path('account/',include('account.urls'))

]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)