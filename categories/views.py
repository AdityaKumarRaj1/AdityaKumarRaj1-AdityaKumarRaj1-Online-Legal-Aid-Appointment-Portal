"""Views for legal categories."""
from django.shortcuts import render
from .models import LegalCategory


def category_list(request):
    """List all active legal categories."""
    categories = LegalCategory.objects.filter(is_active=True)
    return render(request, 'categories/category_list.html', {
        'categories': categories
    })
