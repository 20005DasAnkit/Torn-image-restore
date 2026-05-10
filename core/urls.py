from django.urls import path
from . import views

urlpatterns = [

    # HOME
    path(
        '',
        views.home,
        name='home'
    ),

    # UPLOAD + AI RESTORATION
    path(
        'upload/',
        views.upload,
        name='upload'
    ),

    # GALLERY
    path(
        'gallery/',
        views.gallery,
        name='gallery'
    ),

    # DASHBOARD
    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    # PROFILE
    path(
        'profile/',
        views.profile,
        name='profile'
    ),

    # TESTIMONIALS
    path(
        'testimonials/',
        views.testimonials,
        name='testimonials'
    ),

    # FAQ
    path(
        'faq/',
        views.faq,
        name='faq'
    ),

    # PDF DOWNLOAD
    path(
        'download/',
        views.download_pdf,
        name='download_pdf'
    ),

    # DELETE MULTIPLE IMAGES
    path(
        'delete-multiple/',
        views.delete_images,
        name='delete_images'
    ),
]