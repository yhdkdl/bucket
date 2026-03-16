from django.db import models
from django.contrib.auth.models import User


class BucketList(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    budget = models.CharField(max_length=50)
    group_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def __str__(self):
        return self.name


class BucketItem(models.Model):
    bucket_list = models.ForeignKey(
        BucketList,
        on_delete=models.CASCADE,
        related_name="items"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    completed = models.BooleanField(default=False)
    photo = models.ImageField(upload_to="bucket_photos/", null=True, blank=True)

    def __str__(self):
        return self.title