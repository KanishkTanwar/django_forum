from django.conf import settings
from django.db import models
from django.urls import reverse
from django.db import models
import misaka
from groups.models import Group

from django.contrib.auth import get_user_model
User = get_user_model()  # it gives current model, like this is a user we played
# with in django section where in full UserForm we only fills Username email image
# and password

# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)
    group = models.ForeignKey(Group, related_name='posts', null=True,
                              blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.message

    def save(self,*args, **kwargs):
        self.message_html = misaka.html(self.message)  # remove html tag
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('posts:single', kwargs={'username': self.user.username,
                                               'pk': self.pk})

    class Meta:
        ordering = ["-created_at"]
        unique_together = ["user", "message"]  # this ensures user and message will be same for all objets
