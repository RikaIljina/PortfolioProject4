from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.http import HttpResponseRedirect
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

from mainpage.utils import get_page_obj, sort_by, get_page_context
from entries.models import Entry
from entries.utils import get_published_entries, get_all_entries
from comments.forms import CommentForm
from comments.utils import process_comment_form

from .forms import ProfileForm


def user_profile(request, username):
    """
    View function to display a user's profile page

    This function retrieves the profile and entries of a specified user and
    renders the profile page with the relevant context. If the user has no
    entries, the context is prepared accordingly.

    Args:
        request (HttpRequest): The HTTP request object.
        username (str): The username of the user whose profile is to be
            displayed.

    Returns:
        HttpResponse: The HTTP response object containing the rendered profile
            page.

    Raises:
        Http404: If the user with the specified username does not exist.
    """
    
    user = get_object_or_404(User.objects.all(), username=username)
    profile = user.profile
    # Tells the sidebar to enable sorting buttons for the user entries
    enable_sorting = True
    # Makes sure the 'reset filter' button redirects to profile page when
    # deleting sorting
    profile_view = True

    # Only get entries if the user has added at least one entry
    if hasattr(user, "all_entries"):
        entries = get_published_entries(
            request, user.all_entries, get_comments=False
        )
        entries, sorted_param, page_obj, users, tags = get_page_context(
                                                            request, entries)

        context = {
            "profile": profile,
            "users": users,
            "tags": tags,
            "page_obj": page_obj,
            "sorted_param": sorted_param,
            "enable_sorting": enable_sorting,
            "profile_view": profile_view,
        }
    else:
        context = {
            "profile": profile,
            "users": users,
            "tags": tags,
            "profile_view": profile_view,
        }

    return render(request, "users/profile.html", context)


def dashboard_new_user(request):
    return HttpResponseRedirect(
        reverse("edit_profile", args=[request.user.username])
    )


def dashboard(request, username):
    if not request.user.is_authenticated or username != request.user.username:
        raise PermissionDenied

    user = request.user
    profile = user.profile
    dashboard_view = True
    enable_sorting = True

    # fields = user._meta.get_fields()
    # for field in fields:
    #     print(field)
    # print(user.all_entries)
    if hasattr(user, "all_entries"):
        # user.all_entries.all()
        # messages.info(request, 'Getting all entries')
        entries = get_all_entries(
            request, user.all_entries, get_comments=False
        )
        most_liked = (
            Entry.objects.annotate(likes_received=Count("all_likes"))
            .order_by("-likes_received")
            .first()
        )
        most_recent = Entry.objects.order_by("-created_on").first()
        entries, sorted_param = sort_by(request, entries)

        # if request.GET.get('newEntry'):
        #     return HttpResponseRedirect(reverse('new_entry'))

        # if request.GET.get('liked') and request.user.is_authenticated:
        #     return save_like(request)
        # Deactivate sidebar!!
        page_obj = get_page_obj(request, entries)
        # users = get_username_list()
        # tags = get_all_tags()

        context = {
            "profile": profile,
            # 'entries': entries,
            "most_liked": most_liked,
            "most_recent": most_recent,
            "page_obj": page_obj,
            "sorted_param": sorted_param,
            "dashboard_view": dashboard_view,
            "enable_sorting": enable_sorting,
        }
    else:
        context = {
            "profile": profile,
            "dashboard_view": dashboard_view,
            "enable_sorting": enable_sorting,
        }

    return render(request, "users/dashboard.html", context)


def dashboard_entry(request, username, slug):
    if not request.user.is_authenticated or username != request.user.username:
        raise PermissionDenied

    entry = get_object_or_404(
        get_all_entries(request, request.user.all_entries), slug=slug
    )
    old_files = entry.old_files
    print("In details:")
    print(old_files.items())
    sorted_files = dict(
        sorted(old_files.items(), key=lambda item: item[1][1], reverse=True)
    )
    print(sorted_files)
    modal_text = f'Are you sure you want to delete "{entry.title}"? This action cannot be undone!'
    modal_title = f'Delete "{entry.title}"?'
    dashboard_view = True

    comments = entry.all_comments.select_related("author", "author__profile")

    # if request.GET.get('edit'):
    #     return HttpResponseRedirect(reverse('edit_entry', args=[username, slug]))
    if request.method == "POST":
        process_comment_form(request, entry)
        # TODO: make sure to go back the same path, via js
        # return redirect(f"{reverse('dashboard_entry', args=[username, slug])}")
        return redirect('dashboard_entry', username=username, slug=slug)

    comment_form = CommentForm()

    context = {
        "entry": entry,
        "old_files": sorted_files,
        "comments": comments,
        "comment_form": comment_form,
        "modal_text": modal_text,
        "modal_title": modal_title,
        "dashboard_view": dashboard_view,
    }

    return render(request, "users/dashboard_entry.html", context)


def edit_profile(request, username):
    if not request.user.is_authenticated or username != request.user.username:
        raise PermissionDenied

    profile = request.user.profile
    # id = profile.pic.public_id

    if request.method == "POST" and profile.user == request.user:
        profile_form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile,
            new_file=request.FILES.get("pic"),
        )
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)

            # if request.FILES.get('pic'):
            #     print(cloudinary.uploader.destroy(id, invalidate=True))
            profile.save()
            messages.success(request, "Your profile has been saved.")

        else:
            print("not valid")
            # print(profile_form.errors.as_data())
            messages.error(request, "There was an error saving your profile.")

        # print(request.POST)
        # return HttpResponseRedirect(reverse('dashboard', args=[username]))

    else:
        profile_form = ProfileForm(
            instance=profile,
            initial={
                "bio": profile.bio,
                "pic": profile.pic,
                "website": profile.website,
                "email": profile.email,
            },
        )

    context = {
        "profile": profile,
        "profile_form": profile_form,
    }

    return render(request, "users/profile_form.html", context)


def user_favorites(request, username):
    if not request.user.is_authenticated or username != request.user.username:
        raise PermissionDenied

    # if request.GET.get('liked') and request.user.is_authenticated:
    #     return save_like(request)
    # entries = get_published_entries(request, request.user.liked.all(), get_comments=False)
    likes = request.user.liked.select_related("entry").annotate(
        likes_received=Count("entry__all_likes", distinct=True),
        comments_received=Count("entry__all_comments", distinct=True),
    )
    is_favorite = 1

    page_obj = get_page_obj(request, likes)
    print(page_obj[0].entry.author.username)

    context = {  # 'likes': likes,
        "page_obj": page_obj,
        "is_favorite": is_favorite,
    }

    return render(request, "users/dashboard_user_likes.html", context)


# TODO: Where to put comments and likes? move utils! make like snippets!


def user_comments(request, username):
    if not request.user.is_authenticated or username != request.user.username:
        raise PermissionDenied

    # if request.GET.get('liked') and request.user.is_authenticated:
    #     return save_like(request)

    comments = request.user.commenter.select_related("entry")

    page_obj = get_page_obj(request, comments, 10)

    context = {  # 'comments': comments,
        "page_obj": page_obj,
    }

    return render(request, "users/dashboard_user_comments.html", context)
