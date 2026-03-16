from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import BucketList, BucketItem

from services.ai_generator import generate_bucket_activities
import json


@api_view(["POST"])
def generate_bucket(request):
    try:
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

        # Call AI service
        ai_text = generate_bucket_activities(name, location, budget, group_type)

        # Validate AI response
        if not ai_text:
            return Response({"error": "AI returned empty response"}, status=500)

        try:
            activities = json.loads(ai_text)
        except json.JSONDecodeError:
            # If AI returns non-JSON, fallback to mock activities
            activities = [
                {"title": "Visit a famous landmark"},
                {"title": "Try a local restaurant"},
                {"title": "Walk through a city park"},
                {"title": "Take a sunset photo"},
                {"title": "Explore a hidden street"}
            ]

        items_response = []
        for act in activities:
            # act may be string or dict depending on AI
            title = act["title"] if isinstance(act, dict) else str(act)
            item = BucketItem.objects.create(bucket_list=bucket, title=title)
            items_response.append({"title": item.title})

        return Response({"bucket_id": bucket.id, "items": items_response})

    except Exception as e:
        return Response({"error": str(e)}, status=500)
    
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

from django.shortcuts import get_object_or_404

@api_view(["GET"])
def bucket_detail(request, id):
    bucket = get_object_or_404(BucketList, id=id)

    items = BucketItem.objects.filter(bucket_list=bucket)

    items_data = []
    for item in items:
        items_data.append({
            "id": item.id,
            "title": item.title,
            "completed": item.completed,
            "photo": item.photo.url if item.photo else None
        })

    return Response({
        "id": bucket.id,
        "name": bucket.name,
        "location": bucket.location,
        "items": items_data
    })

@api_view(["POST"])
def complete_item(request, id):

    item = get_object_or_404(BucketItem, id=id)

    item.completed = True
    item.save()

    return Response({
        "status": "completed"
    })