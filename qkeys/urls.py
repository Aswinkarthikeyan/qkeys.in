from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    # =========================
    # Django Admin
    # =========================

    path(
        'admin/',
        admin.site.urls
    ),

    # =========================
    # QKeys.in / Properties
    # =========================

    path(
        '',
        include('properties.urls')
    ),

    # =========================
    # Invoice System
    # =========================

    path(
        'invoices/',
        include('invoices.urls')
    ),
]


# =========================
# Media Files - Development
# =========================

if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )