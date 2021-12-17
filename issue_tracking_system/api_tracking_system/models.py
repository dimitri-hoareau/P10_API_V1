from django.db import models

class Contributors(models.Model):
    # ROLE_CHOICES = (
    #     ('1', 'Admin'),
    #     ('2', 'User'),
    # )

    permission = models.CharField(max_length=255)
    # role = models.CharField(max_length=1, choices=ROLE_CHOICES)
    # user 
    # project


class Project(models.Model):

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=255)
    # author


    def __str__(self):
        return self.title


class Issue(models.Model):

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    tag = models.CharField(max_length=255)
    priority = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    created_time = models.DateTimeField(auto_now_add=True)
    # project
    # author
    # assignee


    # category = models.ForeignKey('shop.Category', on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.title


class Comments(models.Model):

    description = models.TextField(blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    # issue
    # author


    # product = models.ForeignKey('shop.Product', on_delete=models.CASCADE, related_name='articles')

    def __str__(self):
        return self.description