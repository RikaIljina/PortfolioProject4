"""
utils.py for the 'Mainpage' app

This module contains mainpage-related functions that are used by the views.

get_page_context(): Prepare and provide context data for views
get_page_obj(): Paginate a given queryset of entries and return the page object
get_all_tags(): Retrieve all tags for published entries and their respective
    counts
sort_by(): Process GET request to sort entries
"""

from django.core.paginator import Paginator
from django.db.models import Count, Q
from taggit.models import Tag

from users.utils import get_all_usernames


def get_page_context(request, entries=None):
    """
    Prepare and provide context data for views

    This function returns different context data depending on whether the
    'entries' parameter is provided. If 'entries' is None, it returns user and
    tag data for filtering purposes. If 'entries' is provided, it sorts the
    entries based on the request parameters, paginates the sorted entries, and
    returns the sorted and paginated entries along with the user and tag data.

    Args:
        request (HttpRequest): The HTTP request object containing metadata
            about the request.
        entries (QuerySet, optional): A queryset of entry objects to be sorted
            and paginated. Defaults to None.

    Returns:
        tuple: If 'entries' is None, returns a tuple containing:
               - dict: A dictionary of all usernames and their profile images.
               - dict: A dictionary of all tags and their respective amounts.

               If 'entries' is provided, returns a tuple containing:
               - QuerySet: The sorted and paginated entries.
               - str: The sorting parameter used.
               - Page: The page object for the paginated entries.
               - dict: A dictionary of all usernames and their profile images.
               - dict: A dictionary of all tags and their respective amounts.
    """

    if entries == None:
        return get_all_usernames(), get_all_tags()

    entries, sorted_param = sort_by(request, entries)
    page_obj = get_page_obj(request, entries)
    users = get_all_usernames()
    tags = get_all_tags()

    return entries, sorted_param, page_obj, users, tags


def get_page_obj(request, entries, amount=12):
    """
    Paginate a given queryset of entries and return the page object

    This function takes a queryset of entries and paginates them according to
    the specified amount per page. It then returns the page object for the
    current page number, which is obtained from the request's GET parameters.

    Args:
        request (HttpRequest): The HTTP request object containing metadata
            about the request, including GET parameters.
        entries (QuerySet): The queryset of entry objects to be paginated.
        amount (int, optional): The number of entries to display per page.
            Defaults to 12.

    Returns:
        Page: A Page object containing the entries for the current page.
    """

    paginator = Paginator(entries, amount)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return page_obj


def get_all_tags():
    """
    Retrieve all tags for published entries and their respective counts

    This function queries the Tag model to annotate each tag with the number
    of published entries associated with it. It filters out tags with no
    published entries and returns a sorted dictionary of tags and their counts.

    Returns:
        dict: A dictionary where keys are tag names and values are the counts
            of published entries associated with each tag.
    """

    tags = Tag.objects.annotate(
        amount=Count("entry", filter=Q(entry__publish=1), distinct=True)
    ).filter(amount__gt=0)

    tag_dict = {
        str(value["name"]): str(value["amount"]) for value in tags.values()
    }
    sorted_tags = dict(sorted(tag_dict.items()))

    return sorted_tags


def sort_by(request, entries):
    """
    Process GET request to sort entries

    This method processes the GET request and sorts the received QuerySet
    with entries accordingly.

    Args:
        request (HttpRequest): The HTTP request object containing metadata
            about the request, including GET parameters.
        entries (QuerySet): The queryset of entry objects to be sorted.

    Returns:
        tuple:  - QuerySet: The received entries, sorted by the GET parameter
                - str: The GET parameter defining the sort order
    """

    if request.GET.get("sorted") == "by_likes":
        entries = entries.annotate(
            count_likes=Count("all_likes", distinct=True)
        ).order_by("-count_likes")
        sorted_param = "?sorted=by_likes"
    elif request.GET.get("sorted") == "by_date":
        entries = entries.order_by("-created_on")
        sorted_param = "?sorted=by_date"
    elif request.GET.get("sorted") == "by_published":
        entries = entries.order_by("publish")
        sorted_param = "?sorted=by_published"
    elif request.GET.get("sorted") == "by_updated":
        entries = entries.order_by("-updated_on")
        sorted_param = "?sorted=by_updated"

    else:
        sorted_param = ""

    return entries, sorted_param
