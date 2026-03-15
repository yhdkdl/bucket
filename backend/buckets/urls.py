from django.urls import path
from .views import bucket_history, generate_bucket

urlpatterns = [
    path("generate/", generate_bucket),
    path("history/", bucket_history, name="bucket-history"),
]
    