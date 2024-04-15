from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('rating', 'review_text', 'created_at', 'updated_at')
    list_filter = ('rating',)
    search_fields = ('review_text',)
# Register your models here.
