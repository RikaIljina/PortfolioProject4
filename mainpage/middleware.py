from django.contrib.auth.models import User
from django.db.models.functions import Lower
from taggit.models import Tag
from django.db.models import Count, Q

# from mainpage.signals import current_usernames, current_tags


# class InitializeUsernamesMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#         self.initialized = False

#     def __call__(self, request):
#         if not self.initialized:
#           #  self.initialize_usernames_list()
#           #  self.initialize_tags()
#             self.initialized = True

#         response = self.get_response(request)
#         return response

# def initialize_usernames_list(self):
#     global current_usernames
#     if not current_usernames:
#         current_usernames.extend(User.objects.values_list(
#             'username', flat=True).order_by(Lower('username')))
#         print('middleware')

# def initialize_tags(self):
#     global current_tags
#     print("trying to init middleware...")
#     if current_tags is None:
#         print(current_tags)
#         current_tags = Tag.objects.annotate(amount=Count('entry', filter=Q(
#            entry__publish=1), distinct=True)).filter(amount__gt=0).order_by('name')
#         print('middleware tags')
#         print(current_tags)
