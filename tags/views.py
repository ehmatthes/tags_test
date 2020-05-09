from django.shortcuts import render

from .models import Tag


def index(request):
    """Show the entire tag hierarchy."""
    all_tags = Tag.objects.all()

    context = {
        'all_tags': all_tags,
    }

    return render(request, 'tags/index.html', context)


def all_tags(request):
    """Simple view to run all_siblings_leaf."""
    all_tags = Tag.objects.all()

    context = {'all_tags': all_tags}

    return render(request, 'tags/all_tags.html', context)