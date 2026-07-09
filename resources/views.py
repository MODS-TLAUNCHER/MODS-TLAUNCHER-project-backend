"""
Views for resources app
"""

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from .models import Resource, ResourceCategory

@login_required
def resource_list(request):
    """List all resources"""
    category_id = request.GET.get('category')
    resource_type = request.GET.get('type')
    
    resources = Resource.objects.filter(is_active=True)
    
    if category_id:
        resources = resources.filter(category_id=category_id)
    if resource_type:
        resources = resources.filter(resource_type=resource_type)
    
    categories = ResourceCategory.objects.all()
    
    context = {
        'resources': resources,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None,
        'selected_type': resource_type,
    }
    return render(request, 'resources/resource_list.html', context)

@login_required
def resource_detail(request, pk):
    """View resource details"""
    resource = get_object_or_404(Resource, pk=pk, is_active=True)
    resource.increment_views()
    
    # Get related resources
    related_resources = Resource.objects.filter(
        is_active=True
    ).exclude(pk=resource.pk)
    
    if resource.category:
        related_resources = related_resources.filter(category=resource.category)
    else:
        related_resources = related_resources.filter(resource_type=resource.resource_type)
    
    related_resources = related_resources[:5]
    
    context = {
        'resource': resource,
        'related_resources': related_resources,
    }
    return render(request, 'resources/resource_detail.html', context)

@staff_member_required
def resource_upload(request):
    """Upload new resource (staff only)"""
    # This would require a form implementation
    return render(request, 'resources/resource_upload.html')