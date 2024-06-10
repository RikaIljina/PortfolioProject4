from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from taggit.managers import TaggableManager
from django.template.defaultfilters import slugify
import cloudinary

STATUS = ((0, "Private"), (1, "Published"))

# Create your models here.


# class Profile(models.Model):
#     '''User profile
#     Must be created automatically when user registers
#     Move to separate "users" app?'''
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     bio = models.TextField(blank=True, null=True)
#     # TODO: limit image size
#     pic = CloudinaryField('image', default='placeholder')
#     joined = models.DateTimeField(auto_now_add=True)
#     social = models.URLField(blank=True, null=True)
#     email = models.EmailField(blank=True, null=True)

#     def __str__(self) -> str:
#         return f"User profile of {self.user.username}"


class Entry(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="entries")
    title = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    audio_file = CloudinaryField('raw', resource_type='auto', format='mp3')
    description = models.TextField()
    tags = TaggableManager(verbose_name='Tags')
    slug = models.SlugField(max_length=250, unique=True, blank=True)
   # likes = models.IntegerField(null=True, default=0)
   # liked_users = models.ManyToManyField(User, through=Like, related_name='liked_entries', blank=True)
    publish = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ["-created_on"]

    # def created_date(self):
    #     ''' Convert DateTime to pure Date '''
    #     return self.created_on.date()
    
      
    def __str__(self):
        return f"{self.title} created by {self.author}"
    
    def save(self, *args, **kwargs):
        # TODO: Check if author already used same title in form in JS file
        #if not self.slug:
        new_slug = f'{self.title}-{self.author.username}'
       # print(new_slug)
        self.slug = slugify(new_slug)
        return super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        print('Trying to delete')
        print(cloudinary.uploader.destroy(self.audio_file.public_id, resource_type = "video", invalidate=True))
        return super().delete(*args, **kwargs)


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="commenter")
    entry = models.ForeignKey(
        Entry, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return (f"{self.author} commented on {self.entry}: " +
                f"{self.content[:15]}...")


class Like(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="liked")
    entry = models.ForeignKey(
        Entry, on_delete=models.CASCADE, related_name="all_likes")
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_on"]


    def save(self, *args, **kwargs):
        '''Checks if the like is valid before saving
        This makes sure that a user cannot like an entry twice and cannot
        like their own entry
        '''
        if self.user.liked.all().filter(entry=self.entry.id).count() != 0 \
            or self.entry.author == self.user:
            print('You already liked it or this is your own entry')
            return
        else:
            self.entry.likes = self.entry.all_likes.count() + 1
            self.entry.save()
            super(Like, self).save(*args, **kwargs)

    def __str__(self):
        return f"Entry {self.entry} liked by {self.user}"
