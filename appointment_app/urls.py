from django.urls import path

from appointment_app.views import index

app_name = "appointment_app"

urlpatterns = [
    path("", view=index, name="appointments"),

]