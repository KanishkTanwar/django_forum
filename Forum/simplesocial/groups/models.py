from django.db import models
from django.conf import settings
from django.urls import reverse  # str representation of url
from django.db import models
from django.utils.text import slugify
import misaka
from django import template
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()
register = template.Library()  # custom template tags like |safe

# MANY TO MANY here we are using Group as a foreign key in Group
# members as well as in posts model so it is a many to many field :D


class Group(models.Model):
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(unique=True, allow_unicode=True)
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False, default='', blank=True)
    members = models.ManyToManyField(User, through="GroupMember")  # through is like related_name to a whole model

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)  # remove spaces and lowercase
        self.description_html = misaka.html(self.description)  # remove tags like <a> </a>
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        # will create url for specific model
        # delete not works because there is no view to url after delete
        # work around use success_url this can be work with different views too
        # so either use get_abs or success
        return reverse('groups:single', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']  # sort result by order of the name


class GroupMember(models.Model):
    group = models.ForeignKey(Group, related_name='membership', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_groups', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('group', 'user')  # group and user are unique together i guess
