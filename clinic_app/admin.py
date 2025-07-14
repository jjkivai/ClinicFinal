from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin

# Register your models here.
from clinic_app.models import Article


from markdownx.widgets import MarkdownxWidget
from django import forms

class NoCssMarkdownxWidget(MarkdownxWidget):
    class Media:
        js = {}  # Only include JS
        css = {}  # Don't include CSS

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = "__all__"
        widgets = {
            'content': NoCssMarkdownxWidget()
        }

@admin.register(Article)
class ArticleAdmin(MarkdownxModelAdmin):
    form = ArticleForm
    list_display = ('title', 'created_at')
    search_fields = ('title', 'content')
    ordering = ('-created_at',)
    # fields = ('title', 'content', 'created_at')
    readonly_fields = ('created_at',)
    fieldsets = (
        
        (None, {
            'fields': ('title','published','content',),
            'classes': ('wide',),
        }),
    )

    class Media:
        css = {
            'all': ('css/markdownx_output.css',),
        }