from django.db import models
from django.urls import reverse

from django.conf import settings
from PIL import Image

User = settings.AUTH_USER_MODEL

class Profile(models.Model):
    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDER_CHOICES = [
        (GENDER_MALE, ("Male")),
        (GENDER_FEMALE, ("Female")),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=500)
    city = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to="avatars/",
                               null=True, blank=True, default="avatars/default.jpg")
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES,
                                              null=True, blank=True)
    phone = models.CharField(max_length=32, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return self.user.name
    

    def get_absolute_url(self):
        return reverse(
            'profile:profile-view', kwargs={
            'pk': self.pk})
    # def save(self, *args, **kwargs):
    #     super().save()

    #     img = Image.open(self.avatar.path)

    #     if img.height > 100 or img.width > 100:
    #         new_img = (100, 100)
    #         img.thumbnail(new_img)
    #         img.save(self.avatar.path)