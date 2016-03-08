from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Userprofile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    file = models.FileField(upload_to='./data/')
    labelfile = models.FileField(upload_to='./data/', blank=True)

    def __unicode__(self):
        return u"%s" % self.user.username

    def getname(self):
        return self.user.username


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Userprofile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=User)