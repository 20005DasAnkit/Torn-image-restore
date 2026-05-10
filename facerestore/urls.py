from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    # ADMIN PANEL
    path(
        'admin/',
        admin.site.urls
    ),

    # CORE APP URLS
    path(
        '',
        include('core.urls')
    ),

]


# MEDIA FILES
if settings.DEBUG:

    urlpatterns += static(

        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT

    )