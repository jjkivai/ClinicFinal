from django.urls import path

from clinic_app.views import index
from django.views.generic import TemplateView

app_name = "clinic_app"

urlpatterns = [
    path("", view=index, name="home"),
    path("about-us/", view=TemplateView.as_view(template_name='about-us.html'), name="about-us"),
    path("education/", view=TemplateView.as_view(template_name='education-COMING SOON.html'), name="education"),
]