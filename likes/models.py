from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from taggit.managers import TaggableManager
#from django.template.defaultfilters import slugify
from django.utils.text import slugify
import cloudinary
from unidecode import unidecode
from entries.models import Entry