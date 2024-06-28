from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Comment

# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    
    # TODO: Fix prefetch!
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related(
            'author').select_related(
                'entry').prefetch_related(
                    'author__commenter').all()
        return queryset