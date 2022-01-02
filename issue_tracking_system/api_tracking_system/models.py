from django.db import models
from django.conf import settings

class Project(models.Model):

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=255)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Contributors(models.Model):
    # ROLE_CHOICES = (
    #     ('ADMIN', 'Admin'),
    #     ('USER', 'User'),
    # )

    permission = models.CharField(max_length=255)
    # role = models.CharField(max_length=5, choices=ROLE_CHOICES)


    # project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    # user 


class Issue(models.Model):

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    tag = models.CharField(max_length=255)
    priority = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    created_time = models.DateTimeField(auto_now_add=True)


    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # assignee

    def __str__(self):
        return self.title


class Comments(models.Model):

    description = models.TextField(blank=True)
    created_time = models.DateTimeField(auto_now_add=True)    
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.description




# table through
# https://docs.djangoproject.com/fr/4.0/topics/db/models/