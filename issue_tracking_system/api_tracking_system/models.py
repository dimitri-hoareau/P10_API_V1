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
    PERMISSION_CHOICE = (
        ('READ_ONLY', 'Read only'),
        ('CREATE_READ_UPDATE_DELETE', 'Create / Read / Update /Delete'),
    )
    # ROLE_CHOICES = (
    #     ('CONTRIBUTOR', 'Contributor'),
    #     ('AUTHOR', 'Author'),
    # )

    # permission = models.CharField(max_length=255)
    # role = models.CharField(max_length=11, choices=ROLE_CHOICES)
    permission = models.CharField(max_length=60, choices =PERMISSION_CHOICE)
    role = models.CharField(max_length=50)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, 
        related_name="followed_by", 
        on_delete=models.CASCADE)



class Issue(models.Model):

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    tag = models.CharField(max_length=255)
    priority = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    created_time = models.DateTimeField(auto_now_add=True)


    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assignee = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, 
        related_name="assignee", 
        on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comments(models.Model):

    description = models.TextField(blank=True)
    created_time = models.DateTimeField(auto_now_add=True)    
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.description

