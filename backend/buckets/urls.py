from django.urls import path
from .views import (
    generate_bucket,
    bucket_history,
    bucket_detail,
    complete_item
)

urlpatterns = [
    path("generate/", generate_bucket),
    path("history/", bucket_history),
   path("<int:id>/", bucket_detail),
      path("items/<int:id>/complete/", complete_item),
]