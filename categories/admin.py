"""Admin configuration for categories app."""
from django.contrib import admin
from .models import LegalCategory


@admin.register(LegalCategory)
class LegalCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'lawyer_count', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)
