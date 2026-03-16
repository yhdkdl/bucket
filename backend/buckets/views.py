from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import BucketList, BucketItem
from PIL import Image
import io

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
    item.completed = not item.completed  # <-- toggle True/False
    item.save()
    return Response({"status": "success", "completed": item.completed})

@api_view(["POST"])
def upload_photo(request, id):

    item = get_object_or_404(BucketItem, id=id)

    if "photo" in request.FILES:
        item.photo = request.FILES["photo"]
        item.save()

        return Response({
            "status": "photo uploaded",
            "photo_url": item.photo.url
        })

    return Response({"error": "No photo provided"}, status=400)

@api_view(["GET"])
def generate_collage(request, bucket_id):
    """
    Generate a collage image from all completed photos in a bucket.
    Query param: type=horizontal|vertical
    """
    collage_type = request.GET.get("type", "horizontal")
    
    try:
        bucket = BucketList.objects.get(id=bucket_id)
    except BucketList.DoesNotExist:
        return Response({"error": "Bucket not found"}, status=404)

    # Filter completed items with photos
    completed_items = BucketItem.objects.filter(bucket_list=bucket, completed=True, photo__isnull=False)
    if not completed_items.exists():
        return Response({"error": "No completed photos to generate collage"}, status=400)

    # Open all images
    images = []
    for item in completed_items:
        img = Image.open(item.photo.path).convert("RGB")
        images.append(img)

    if collage_type == "horizontal":
        # Arrange images horizontally
        max_height = 300
        resized_images = []
        total_width = 0
        for img in images:
            img_ratio = img.width / img.height
            new_width = int(max_height * img_ratio)
            resized_img = img.resize((new_width, max_height))
            resized_images.append(resized_img)
            total_width += new_width
        
        collage_img = Image.new("RGB", (total_width, max_height), (255, 255, 255))
        x_offset = 0
        for img in resized_images:
            collage_img.paste(img, (x_offset, 0))
            x_offset += img.width

    elif collage_type == "vertical":
        # Arrange images vertically
        max_width = 300
        resized_images = []
        total_height = 0
        for img in images:
            img_ratio = img.height / img.width
            new_height = int(max_width * img_ratio)
            resized_img = img.resize((max_width, new_height))
            resized_images.append(resized_img)
            total_height += new_height
        
        collage_img = Image.new("RGB", (max_width, total_height), (255, 255, 255))
        y_offset = 0
        for img in resized_images:
            collage_img.paste(img, (0, y_offset))
            y_offset += img.height

    else:
        return Response({"error": "Invalid collage type"}, status=400)

    # Save to BytesIO
    buffer = io.BytesIO()
    collage_img.save(buffer, format="PNG")
    buffer.seek(0)

    preview = request.GET.get("preview", "false").lower() == "true"
    response = HttpResponse(buffer, content_type="image/png")
    if preview:
        response["Content-Disposition"] = "inline; filename=collage.png"
    else:
        response["Content-Disposition"] = "attachment; filename=collage.png"

    return response