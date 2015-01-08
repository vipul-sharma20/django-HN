from django.contrib.auth.models import User
from django.db import models

class Contact(models.Model):

    first_name = models.CharField(max_length=255, )
    last_name = models.CharField(max_length=255,)
    # profile_pic = models.ImageField(upload_to='pictures', blank=True)
    email = models.EmailField()

    def __str__(self):
        return ' '.join([self.first_name, self.last_name, ])


class UserProfile(models.Model):

    user = models.OneToOneField(User, unique=True)
    location = models.CharField(max_length=140)
    gender = models.CharField(max_length=140)
    reputation = models.IntegerField(default=1)

    #profile_picture = models.ImageField(upload_to='%Y/%m/%d', blank=True, default = '/home/vipul/Photo13892.jpg')

    def __str__(self):
        return 'Profile of user : %s' % self.user.username


class Articles(models.Model):

    description = models.CharField(max_length=255)
    link = models.URLField(max_length=255)
    uploader = models.ForeignKey(User)
    time_stamp = models.DateTimeField()
    votes = models.PositiveIntegerField(default=1)

class Like(models.Model):

    user = models.ForeignKey(User)
    article = models.ForeignKey(Articles)
    date = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):

    user = models.ForeignKey(User)
    article = models.ForeignKey(Articles)
    date = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=255,)
