"""
utils.py for the 'Entries' app

This module contains entry-related functions that are used by the views.

get_published_entries(): Process a queryset to filter, prefetch/select data and
    add annotations
get_all_entries(): Process queryset for authenticated users, add related data
    and annotations
"""

from django.db.models import Count, Q


def get_published_entries(request, source, get_likes=True, get_comments=True):
    """
    Process a queryset to filter, prefetch/select data and add annotations

    Args:
        request (HttpRequestObject): The request object
        source (queryset): The relevant queryset to process; could be
            Entry.objects or user.all_entries
        get_likes (bool, optional): Whether to annotate with 'already_liked',
            which can be 1 or 0, depending on whether user liked the entry or
            not. Defaults to True.
        get_comments (bool, optional): Whether to prefetch the entry comments.
            Only needed on the entry details page. Defaults to True.

    Returns:
        entries (queryset): A queryset with published entries along with a
            variety of annotations and related data.
    """

    # likes_received and comments_received inform the like_comment_summary
    # snippet of the 'likes' app
    if request.user.is_authenticated and get_likes and get_comments:
        entries = (
            source.filter(publish=1)
            .annotate(
                already_liked=Count(
                    "all_likes",
                    filter=Q(all_likes__user=request.user),
                    distinct=True,
                ),
                likes_received=Count("all_likes", distinct=True),
                comments_received=Count("all_comments", distinct=True),
            )
            .select_related("author")
            .select_related("author__profile")
            .prefetch_related("tagged_items__tag", "tags", "all_comments")
        )

    elif request.user.is_authenticated and not get_comments:
        entries = (
            source.filter(publish=1)
            .annotate(
                already_liked=Count(
                    "all_likes",
                    filter=Q(all_likes__user=request.user),
                    distinct=True,
                ),
                likes_received=Count("all_likes", distinct=True),
                comments_received=Count("all_comments", distinct=True),
            )
            .select_related("author")
            .select_related("author__profile")
            .prefetch_related("tagged_items__tag", "tags")
        )

    elif get_comments:
        entries = (
            source.filter(publish=1)
            .annotate(
                likes_received=Count("all_likes", distinct=True),
                comments_received=Count("all_comments", distinct=True),
            )
            .select_related("author")
            .select_related("author__profile")
            .prefetch_related("tagged_items__tag", "tags", "all_comments")
        )

    else:
        entries = (
            source.filter(publish=1)
            .annotate(
                likes_received=Count("all_likes", distinct=True),
                comments_received=Count("all_comments", distinct=True),
            )
            .select_related("author")
            .select_related("author__profile")
            .prefetch_related("tagged_items__tag", "tags")
        )

    return entries


def get_all_entries(request, source, get_comments=True):
    """
    Process queryset for authenticated users, add related data and annotations

    Args:
        request (HttpRequestObject): The request object
        source (queryset): The relevant queryset to process; should be
            request.user.all_entries
        get_comments (bool, optional): Whether to prefetch the entry comments.
            Only needed on the entry details page. Defaults to True.

    Returns:
        entries (queryset): A queryset with the user's published and private
            entries along with a variety of annotations and related data.
    """

    if request.user.is_authenticated:
        if get_comments:
            entries = (
                source.annotate(
                    likes_received=Count("all_likes", distinct=True),
                    comments_received=Count("all_comments", distinct=True),
                )
                .select_related("author")
                .select_related("author__profile")
                .prefetch_related("tagged_items__tag", "tags", "all_comments")
            )

        else:
            entries = (
                source.annotate(
                    likes_received=Count("all_likes", distinct=True),
                    comments_received=Count("all_comments", distinct=True),
                )
                .select_related("author")
                .select_related("author__profile")
                .prefetch_related(
                    "tagged_items__tag",
                    "tags",
                )
            )

        return entries
