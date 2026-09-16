from django.urls import path

from .views import google_verification, home, robots_txt, sitemap_xml

urlpatterns = [
    path('', home, name='home'),
    path('google8e77f9c223e6e972.html', google_verification, name='google_verification'),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('sitemap.xml', sitemap_xml, name='sitemap_xml'),
]

