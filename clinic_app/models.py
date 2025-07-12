from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from bs4 import BeautifulSoup
from django.utils.text import slugify
import re
from django.utils.html import strip_tags
from markdown import markdown
from django.utils.timesince import timesince
from django.utils.timezone import now
class Article(models.Model):

    TYPE_CHOICES = (
        ('artcile', 'Article'),
        ('educational', 'Educational'),
        ('announcement', 'Announcement'),
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='artcile')

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = MarkdownxField()
    created_at = models.DateTimeField(auto_now_add=True)

    def summary(self, max_words=30):
        # Optional: remove the first Markdown header
        content = re.sub(r'^#{1,6} .*?\n+', '', self.content, count=1)
        html = markdown(content)
        text = strip_tags(html)
        words = text.split()
        return ' '.join(words[:max_words]) + ('...' if len(words) > max_words else '')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    @property
    def time_stamp(self):

        if not self.created_at:
            return "Unknown time"
        delta = timesince(self.created_at, now()).split(",")[0]  # Only take the first unit
        return f"{delta.strip()} ago"
    
    @property
    def rendered_content(self):
        return markdownify(self.content)
    
    @property
    def cover_image(self):
        html = markdownify(self.content)
        soup = BeautifulSoup(html, "html.parser")
        img = soup.find("img")
        return img['src'] if img else None