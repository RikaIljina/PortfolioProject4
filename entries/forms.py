from django import forms
from django.forms import TextInput, Textarea, RadioSelect, FileInput, EmailInput, URLInput,  NullBooleanSelect, CheckboxInput
from django.utils.translation import gettext_lazy as _
from cloudinary.forms import CloudinaryFileField
from django_summernote.widgets import SummernoteWidget
import cloudinary

from .models import Entry


class EntryForm(forms.ModelForm):
    """
    Form class for users to add a new entry 
    """
    keep_file = forms.BooleanField(required=False, label='Keep previous file?')

    class Meta:
        """
        Specify the django model and order of the fields
        """
        model = Entry
        fields = ('title', 'description', 'audio_file', 'tags', 'publish', 'old_files')
        widgets = {
            "title": TextInput(attrs={"class":"flex-fill form-control me-3"}),
            "description": SummernoteWidget(attrs={"rows":"3", "class":"flex-fill form-control me-3", "type":"text", "name":"description"}),
            "audio_file": FileInput(attrs={"class":"flex-fill form-control me-3"}),
            "tags": TextInput(attrs={"class":"flex-fill form-control me-3"}),
            "publish": RadioSelect(),
            "keep_file":  CheckboxInput(),
            }
        
        labels = {
            'title': _('Title'),
            'description': _('Description'),
            'audio_file': _('New audio file (mp3)'),
            'tags': _('Tags (comma-separated)'),
            'publish': _('Publicity'),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.new_file = kwargs.pop('new_file', None)
        #self.keep_file = kwargs.pop('keep_file', False)
        super(EntryForm, self).__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data.get('title')
        print(f'new title {title}')
        print(Entry.objects.filter(author=self.user, title=title))
        instance = self.instance
        if Entry.objects.filter(author=self.user, title=title).exclude(id=instance.id).exists():
            raise forms.ValidationError("You have already used this title for another song.")
        return title
    
    def save(self, commit=True):
        print('entering class')
        instance = super(EntryForm, self).save(commit=False)
        instance.author = self.user
        #print(f'Instance in save: {instance}')
        keep_file = self.data.get('keep_file')
        
        if self.new_file and keep_file:
            old_id = self.initial['audio_file'].public_id

            instance.old_files[old_id] = self.initial['audio_file'].url
 
            print(instance.old_files)
            
            #print(f'changed file: {self.new_file}, old: {old_id}')
            instance.save()
            #print(cloudinary.uploader.destroy(old_id, resource_type = "video", invalidate=True))
            # print(cloudinary.uploader.destroy(self.old_id, resource_type = "video", invalidate=True))
        elif self.new_file:
            old_id = self.initial['audio_file'].public_id

           # instance.old_files[old_id] = self.initial['audio_file'].url
 
           # print(instance.old_files)
            
            #print(f'changed file: {self.new_file}, old: {old_id}')
            instance.save()
            print(cloudinary.uploader.destroy(old_id, resource_type = "video", invalidate=True))
            
        else:
            print('just saving in class')
            instance.save()
            
        if commit:
            print('saving in class with commit true')
            instance.save()

        return instance
