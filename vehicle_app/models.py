from django.db import models


class Brand(models.Model):
    page_id = models.CharField(max_length=255, unique=True)
    page_name = models.CharField(max_length=255)
    url = models.URLField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.page_name}"


class Car(models.Model):
    brand = models.ForeignKey(Brand, related_name='cars', on_delete=models.CASCADE)
    name = models.CharField(max_length=255,unique=True)
    model = models.CharField(max_length=255)
    year = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} {self.model} ({self.year})"
