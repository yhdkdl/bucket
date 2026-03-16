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
    path("detail/<int:bucket_id>/", bucket_detail),
    path("complete/<int:item_id>/", complete_item),
]