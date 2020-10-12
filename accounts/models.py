from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.conf import settings
from django.db.models import Q

# Create your models here.
class Profile(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=False,null=False)
    age = models.PositiveIntegerField(blank=False,null=False)
    location = models.CharField(max_length=60)
    publish_date = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(blank=False,null=False, max_length=20)
    your_country = models.CharField(max_length=50, blank=False)    
    image = models.ImageField(blank=False,null=False, upload_to="profile_image")
    cover_photo = models.ImageField(blank=True, upload_to="cover_photo")
    followers = models.ManyToManyField(User, related_name='accounts_profile', blank=True)
    following = models.ManyToManyField(User, related_name='accounts_profile_following', blank=True) 

    def total_followers(self):
        return self.followers.count()

    def total_following(self):
        return self.following.count()
        
    def __str__(self):
        return self.user.username

    def save(self):
        super().save()

        img = Image.open(self.image.path)
        if img.height > 160 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)