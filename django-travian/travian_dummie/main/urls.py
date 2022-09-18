# Here we define the paths to our webpages

from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("<int:id>", views.resource, name="aldea"),
    path("increase/", views.dorf, name="aldea"),
    path("production/", views.dorf, name="aldea"),
    path("create", views.create, name="aldea"),
]

# admin
# user = metol
# mail = metolag@gmail.com
# pass = 1234