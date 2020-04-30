from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator

# Create your models here.


# Extending the existing user model to add
# n:m relations
# Reference: https://bit.ly/3f0TeWp
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    resources = models.ManyToManyField('Resource')
    comments = models.ManyToManyField('Comment')


class Category(models.Model):
    category_name = models.CharField(max_length=20)

    def __str__(self):
        return self.category_name


class Type(models.Model):
    type_name = models.CharField(max_length=20)

    def __str__(self):
        return self.type_name


class Resource(models.Model):
    resource_name = models.CharField(max_length=100)
    resource_description = models.TextField()
    resource_author = models.CharField(max_length=50)
    resource_image = models.ImageField()
    resource_votes = models.IntegerField(default=0)
    resource_url = models.URLField()
    resource_price = models.DecimalField(
        default=0, max_digits=4, decimal_places=2)
    resource_discount = models.PositiveSmallIntegerField(
        default=0, validators=[MaxValueValidator(100)])
    resource_creation_date = models.DateField(auto_now_add=True)
    post_autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
    )
    resource_category = models.ManyToManyField(Category)
    resource_type = models.ForeignKey(Type, on_delete=models.CASCADE,)


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    comment_text = models.TextField()
    comment_date = models.DateField(auto_now_add=True)
    comment_votes = models.IntegerField(default=0)
    resource_id = models.ForeignKey(Resource, on_delete=models.CASCADE,)
    comment_author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        unique_together = ['comment_id', 'resource_id']


# class Resource_vote(models.Model):
#     vote_type = models.PositiveSmallIntegerField(
#         default=0, min_value=-1, max_value=1)
#     resource_id = models.ForeignKey(Resource, on_delete=model.CASCADE,)
#     user_id = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#     )

#     class Meta:
#         unique_together = ['resource_id', 'user_id']


# class Comment_vote(models.Model):
#     vote_type = models.PositiveSmallIntegerField(
#         default=0, min_value=-1, max_value=1)
#     comment_id = models.ForeignKey(Comment, on_delete=model.CASCADE,)
#     resource_id = models.ForeignKey(Resource, on_delete=model.CASCADE,)
#     user_id = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#     )

#     class Meta:
#         unique_together = ['comment_id', 'resource_id', 'user_id']
