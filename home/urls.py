# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('',
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^empresa/', empresaHomePageView.as_view(), name='empresa'),
    url(r'^faq/', faqHomePageView.as_view(), name='faq'),
    url(r'^eventos/', eventosHomePageView.as_view(), name='eventos'),
    url(r'^servicios/', serviciosHomePageView.as_view(), name='eventos'),
    url(r'^contact/', contactHomePageView.as_view(), name='contact'),
    url(r'^casamatriz/', casa_matrizHomePageView.as_view(), name='casamatriz'),
    url(r'^chinandega/', chinandegaHomePageView.as_view(), name='chinandega'),
    url(r'^montoya/', montoyaHomePageView.as_view(), name='montoya'),
)