from django.db import models
import re

class UserManager(models.Manager):
    def validator(self, postdata):
        errors={}
        if len(postdata['user_name']) < 2:
            errors['user_name'] = "User Name must be longer than 2 characters"
        if len(postdata['pw']) < 8:
            errors['pw'] ="Password must be at least 8 characters long"
        return errors



class User(models.Model):
    user_name = models.CharField(max_length=225)
    password = models.CharField(max_length=225)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Post(models.Model):
    post = models.ImageField(null=False, blank=False, upload_to="images")
    liked = models.ManyToManyField(User, default=None, blank=True, related_name='liked')

    def total_likes(self):
        return self.likes.count()


# choices in value for Like model
LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, default='Like', max_length=100)

