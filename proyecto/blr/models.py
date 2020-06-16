from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.urls import reverse_lazy
from taggit.managers import TaggableManager
from vote.models import VoteModel
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment
from django.urls import reverse

# Extending the existing user model to add
# n:m relations
# Reference: https://bit.ly/3f0TeWp
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)
    
    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('userPage')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Type(models.Model):
    type_name = models.CharField(max_length=20)

    def __str__(self):
        return self.type_name


class Resource(VoteModel, models.Model):
    resource_name = models.CharField(max_length=100)
    resource_description = models.TextField()
    resource_author = models.CharField(max_length=50)
    resource_image = models.ImageField(default="default.png")
    user_saved = models.ManyToManyField(Profile, related_name='votes', blank=True)
    resource_url = models.URLField()
    resource_price = models.DecimalField(
        default=0, max_digits=4, decimal_places=2)
    resource_discount = models.PositiveSmallIntegerField(
        default=0, validators=[MaxValueValidator(100)])
    resource_creation_date = models.DateField(auto_now_add=True)
    post_author = models.ForeignKey(Profile, related_name='post_author', null=True, on_delete=models.SET_NULL)
    resource_slug = models.SlugField(unique=True, max_length=100)
    resource_tags = TaggableManager()
    resource_type = models.ForeignKey(Type, on_delete=models.CASCADE,)
    resource_stars = models.IntegerField(default=0)
    comments = GenericRelation(Comment)

    def __str__(self):
        return self.resource_name
        
    def get_absolute_url(self):
        # return reverse('resource-list', args=[resource.resource_slug])
        return reverse_lazy('resource-list')
        # return reverse ('resource-detail', kwargs={'pk':self.pk})


# class Comment(models.Model):
#     comment_id = models.AutoField(primary_key=True)
#     comment_text = models.TextField()
#     comment_date = models.DateField(auto_now_add=True)
#     comment_votes = models.IntegerField(default=0)
#     resource_id = models.ForeignKey(Resource, on_delete=models.CASCADE,)
#     comment_author = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.SET_NULL,
#         null=True,
#     )

#     class Meta:
#         unique_together = ['comment_id', 'resource_id']

#     def __str__(self):
#         return self.comment_text[:15]+"..."