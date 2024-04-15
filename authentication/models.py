from django.db import models

class Review(models.Model):
    rating = models.PositiveIntegerField(default=0)
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Rating: {self.rating} - Review: {self.review_text[:20]}..."
# Create your models here.

