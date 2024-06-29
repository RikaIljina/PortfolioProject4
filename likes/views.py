from django.shortcuts import get_object_or_404, reverse, redirect
from django.core.exceptions import PermissionDenied

from entries.models import Entry

from .models import Like


def add_like(request, entry_id, current_path=""):
    if not request.user.is_authenticated:
        raise PermissionDenied

    entry = get_object_or_404(
        Entry.objects.filter(publish=1), id=entry_id)

    if request.GET.dict():
        print("...getting...")
        print(request.GET.dict())
        params = f"?{request.GET.urlencode()}"
    else:
        params = ""

    if not request.user.liked.filter(entry__pk=entry_id).exists():
        Like.objects.create(user=request.user, entry=entry)

    return redirect(f"{reverse('home')}{current_path}{params}")


def delete_like_by_entry(request, entry_id, current_path=""):
    if not request.user.is_authenticated:
        raise PermissionDenied
    
    if request.GET.dict():
        params = f"?{request.GET.urlencode()}"
    else:
        params = ""

    like = request.user.liked.filter(entry__pk=entry_id).first()
    like.delete()

    return redirect(f"{reverse('home')}{current_path}{params}")


def delete_like_by_like(request, like_id, current_path=""):
    if not request.user.is_authenticated:
        raise PermissionDenied
    
    if request.GET.dict():
        params = f"?{request.GET.urlencode()}"
    else:
        params = ""

    if request.user.liked.filter(id=like_id).exists():
        like = Like.objects.get(id=like_id)
        like.delete()
    else:
        raise PermissionDenied

    return redirect(f"{reverse('home')}{current_path}{params}")
