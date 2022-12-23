from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=6, blank=True)
    DOB = models.DateField('date of birth', null=True)
    status = models.CharField(max_length=6, blank=True)
    bio = models.TextField(max_length=100, blank=True)
    profilephoto = models.ImageField(upload_to='images/', blank=True, default=f"{user.name}_profilePic.jpg")
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        
        # instance.profile.gender = instance.socialaccount_set.filter(provider='google')[0].extra_data['gender']
        
        # print('----')
        # print(instance.socialaccount_set.filter(provider='google')[0])
        # print('----')
        
        src_dir = r"/Users/nishkarsh/Programming/VS PYTHON/SUTT_Recruitment/Task3-DatingSite/DatingSite/media/images/DefaultPic.jpg"
        dst_dir = f"/Users/nishkarsh/Programming/VS PYTHON/SUTT_Recruitment/Task3-DatingSite/DatingSite/media/{instance.username}_profilePic.jpg"
        
        im1 = Image.open(src_dir)
        im2 = im1.copy()
        im2.save(dst_dir)
        
        instance.profile.profilephoto = f"/{instance.username}_profilePic.jpg"

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()