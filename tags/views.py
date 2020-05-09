from django.shortcuts import render

from .models import Tag


def index(request):
    """Show the entire tag hierarchy."""
    all_tags = Tag.objects.all()

    context = {
        'all_tags': all_tags,
    }

    return render(request, 'tags/index.html', context)