from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'moneycash.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^adminactions/', include('adminactions.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^base/', include('base.urls')),
    url(r'^facturacion/', include('facturacion.urls')),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
