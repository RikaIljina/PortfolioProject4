from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
import cloudinary

from .models import Profile

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(SummernoteModelAdmin):

    list_display = ('user', 'bio', 'pic', 'joined', 'social', 'email',)
    search_fields = ['user__username', 'bio',]
    list_filter = ('user', 'joined')
   # prepopulated_fields = {'slug': ('title', 'author')}
    summernote_fields = ('bio',)

    def save_model(self, request, obj, form, change):
        print('saving profile in admin...')
        print(form.cleaned_data['pic'])
        #print(form.initial['pic'])
        old_pic = form.initial.get('pic')
        if old_pic:
            old_pic = old_pic.public_id
            if old_pic != form.cleaned_data['pic']:
                print('pic has changed')
                print(cloudinary.uploader.destroy(old_pic, invalidate=True))
        super().save_model(request, obj, form, change)

    # def delete_model(self, request, obj):
    #     print(cloudinary.uploader.destroy(obj.audio_file.public_id, resource_type = "video", invalidate=True))
    #     super().delete_model(request, obj)
        
    def delete_queryset(self, request, queryset):
        for obj in queryset:
            print(obj)
            print(obj.pic)
            print(cloudinary.uploader.destroy(obj.pic.public_id, invalidate=True))
        super().delete_model(request, queryset)