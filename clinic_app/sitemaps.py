from django.contrib.sitemaps import Sitemap
from clinic_app.models import Article

class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Article.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.created_at
    
    def location(self, obj):
        return f"/educattion/{obj.slug}/"