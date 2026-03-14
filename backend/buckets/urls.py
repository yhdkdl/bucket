from django.urls import path
from .views import generate_bucket

urlpatterns = [
    path("generate/", generate_bucket),
]