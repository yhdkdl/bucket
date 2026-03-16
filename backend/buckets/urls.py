from django.urls import path
from .views import (
    generate_bucket,
    bucket_history,
    bucket_detail,
    complete_item,
    generate_collage,
    upload_photo
)

urlpatterns = [
    path("generate/", generate_bucket),
    path("history/", bucket_history),
    path("<int:id>/", bucket_detail),
    path("items/<int:id>/complete/", complete_item),
    path("items/<int:id>/upload-photo/", upload_photo),
     path("<int:bucket_id>/collage/", generate_collage, name="generate-collage"),
]