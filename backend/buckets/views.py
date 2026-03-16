from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import BucketList, BucketItem

from services.ai_generator import generate_bucket_activities
import json


@api_view(["POST"])
def generate_bucket(request):

    name = request.data.get("name")
    location = request.data.get("location")
    budget = request.data.get("budget")
    group_type = request.data.get("group_type")

    # create bucket record
    bucket = BucketList.objects.create(
        name=name,
        location=location,
        budget=budget,
        group_type=group_type
    )

    # 🔥 AI generation
    ai_text = generate_bucket_activities(
        name,
        location,
        budget,
        group_type
    )

    # convert AI JSON string → python list
    activities = json.loads(ai_text)

    items_response = []

    # save activities
    for act in activities:
        item = BucketItem.objects.create(
            bucket_list=bucket,
            title=act["title"]
        )

        items_response.append({
            "title": item.title
        })

    return Response({
        "bucket_id": bucket.id,
        "items": items_response
    })

@api_view(["GET"])
def bucket_history(request):
    """
    Returns all bucket lists with their items.
    Currently global; later will filter by user.
    """
    history = []

    # Fetch all buckets from DB
    buckets = BucketList.objects.all().order_by("-created_at")  # newest first

    for bucket in buckets:
        items = BucketItem.objects.filter(bucket_list=bucket)
        item_list = [{"title": item.title} for item in items]

        history.append({
            "bucket_id": bucket.id,
            "name": bucket.name,
            "location": bucket.location,
            "budget": bucket.budget,
            "group_type": bucket.group_type,
            "items": item_list
        })

    return Response(history)

@api_view(["GET"])
def bucket_detail(request, bucket_id):

    try:
        bucket = BucketList.objects.get(id=bucket_id)
    except BucketList.DoesNotExist:
        return Response({"error": "Not found"}, status=404)

    items = BucketItem.objects.filter(bucket_list=bucket)

    item_list = []

    for item in items:
        item_list.append({
            "id": item.id,
            "title": item.title,
            "completed": item.completed,
            "photo": item.photo.url if item.photo else None
        })

    return Response({
        "bucket_id": bucket.id,
        "name": bucket.name,
        "location": bucket.location,
        "items": item_list
    })

@api_view(["POST"])
def complete_item(request, item_id):

    try:
        item = BucketItem.objects.get(id=item_id)
    except BucketItem.DoesNotExist:
        return Response({"error": "Not found"}, status=404)

    item.completed = True
    item.save()

    return Response({"status": "completed"})