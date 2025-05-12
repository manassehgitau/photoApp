from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.dispatch import receiver
from django.db.models.signals import post_save

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', null=True)
    profile_photo = CloudinaryField('image', default='https://images.unsplash.com/photo-1640960543409-dbe56ccc30e2?w=400&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OHx8cHJvZmlsZSUyMGF2YXRhcnxlbnwwfHwwfHx8MA%3D%3D', null=True)
    bio = models.TextField(max_length=300, null=True)
    location = models.CharField(max_length=100, null=True)
    contact = models.CharField(max_length=100, null=True)
    created_on = models.DateTimeField(auto_now_add=True,null=True)
    updated_on = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return f'{self.user.username} profile'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

class Photo(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='photos/')
    tags = models.ManyToManyField('Tag')
    liked_by = models.ManyToManyField(User, related_name='liked_photos', blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)