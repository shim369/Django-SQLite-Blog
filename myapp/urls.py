from django.urls import include, path
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from .sitemaps import (
    BlogPostSitemap,StaticViewSitemap
)
from django.views.generic import TemplateView

sitemaps = {
    'blog': BlogPostSitemap,
    'static': StaticViewSitemap,
}
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bbs.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
	path('sw.js', (TemplateView.as_view(template_name="sw.js",content_type='application/javascript', )), name='sw.js'),
]

# 開発環境下のみ設定
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
