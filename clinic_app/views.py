from django.shortcuts import render, get_object_or_404
from .models import Article

# Create your views here.
def index(request):
    return render(request, "index.html")

def heart_day_view(request):
    return render(request, "heartday.html")

def education_view(request):
    articles = Article.objects.filter(published=True).order_by('-created_at')
    if not articles:
        return render(request, "education.html", {"articles": articles, "message": "No articles available."})
    return render(request, "education.html", {"posts": articles})

def education_detail_view(request, slug):
    article = get_object_or_404(Article, slug=slug, published=True)
    related_articles = Article.objects.exclude(slug=slug, published=True)[:4]  # Get 4 related articles excluding the current one
    if not related_articles:
        related_articles = Article.objects.filter(published=True)[:4]  # Fallback to any 4 articles if none are related
    return render(request, "blog/blog.html", {"article": article, "related_articles": related_articles})