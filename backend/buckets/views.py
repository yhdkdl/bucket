from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import BucketList, BucketItem


@api_view(["POST"])
def generate_bucket(request):

    name = request.data.get("name")
    location = request.data.get("location")
    budget = request.data.get("budget")
    group_type = request.data.get("group_type")

    bucket = BucketList.objects.create(
        name=name,
        location=location,
        budget=budget,
        group_type=group_type
    )

    mock_items = [
        "Visit a famous landmark",
        "Try a local restaurant",
        "Walk through a city park",
        "Take a sunset photo",
        "Explore a hidden street"
    ]

    items_response = []

    for title in mock_items:
        item = BucketItem.objects.create(
            bucket_list=bucket,
            title=title
        )
        items_response.append({
            "title": item.title
        })

    return Response({
        "bucket_id": bucket.id,
        "items": items_response
    })