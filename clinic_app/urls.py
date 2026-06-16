from django.urls import path

from clinic_app.views import education_view, education_detail_view, contact
from django.views.generic import RedirectView, TemplateView

app_name = "clinic_app"

urlpatterns = [
    path("", view=TemplateView.as_view(template_name='index.html'), name="home"),
    path("about-us/", view=TemplateView.as_view(template_name='about-us.html'), name="about-us"),
    path("education/", view=education_view, name="education"),
    path("education/<slug:slug>/", view=education_detail_view, name="education-detail"),
    path("blog/", view=TemplateView.as_view(template_name='blog/blog.html'), name="blog"),
    # path("heart-day/", view=TemplateView.as_view(template_name='heartday.html'), name="heart-day"),
    path("services/", view=TemplateView.as_view(template_name='services.html'), name="services"),
    path("contact-us/", view=contact, name="contact-us"),
    path("contact/", RedirectView.as_view(url='/contact-us/', permanent=False), name="contact"),
]