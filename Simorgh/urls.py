from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib.sitemaps import Sitemap, FlatPageSitemap, GenericSitemap
from Simorgh import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from Simorgh.sitemap import BlogSiteMap


admin.autodiscover()

sitemaps = {
     'pages': BlogSiteMap(['hotels_list', 'profile', 'login', 'logout', 'forgotpass', 'senduser','changepass', 'add_hotel', 'home','my_reservation', 'commision', 'my_comments', 'report', 'contact', 'about', 'cancel'])
}

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^simorgh/', include('Manage.urls')),
    url(r'^simorgh/', include('Reservation.urls')),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
