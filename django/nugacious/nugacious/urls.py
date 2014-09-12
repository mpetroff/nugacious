from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', 'nugacious.views.home', name='home'),
    url(r'^about/', 'nugacious.views.about', name='about'),
    url(r'^comparison/', 'nugacious.views.comparison', name='comparison'),
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt',
        content_type='text/plain')),
    url(r'^sitemap\.xml$', TemplateView.as_view(template_name='sitemap.xml',
        content_type='application/xml')),
)
