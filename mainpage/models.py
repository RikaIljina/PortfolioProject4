from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from taggit.managers import TaggableManager

STATUS = ((0, "Private"), (1, "Published"))

# Create your models here.
class Profile(models.Model):
    '''User profile
    Must be created automatically when user registers
    Move to separate "users" app?'''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    pic = CloudinaryField('image', default='placeholder')
    joined = models.DateTimeField(auto_now_add=True)
    social = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    
    def __str__(self) -> str:
        return f"User profile of {self.user.username}"
    
    
class Entry(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="entries")
    title = models.CharField(max_length=200, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    audio_file = CloudinaryField('audio')
    description = models.TextField()
    tags = TaggableManager()
    slug = models.SlugField(max_length=200, unique=True)
    likes = models.IntegerField(blank=True, null=True)
    publish = models.IntegerField(choices=STATUS, default=0)
    
    class Meta:
        ordering = ["-created_on"]
    
    def __str__(self):
        return f"Entry {self.title} created by {self.author}"
    
    
class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="commenter")
    entry = models.ForeignKey(
        Entry, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-created_on"]
    
    def __str__(self):
        return f"Comment {self.content} written by {self.author}"
    
    
class Like(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="liked")
    entry = models.ForeignKey(
        Entry, on_delete=models.CASCADE, related_name="all_likes")
    created_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-created_on"]
    
    def __str__(self):
        return f"Entry {self.entry} liked by {self.user}"