from django.db import models

# Create your models here.

class Email(models.Model):
    gmail = models.CharField('Gmail', unique=True, max_length=200)
    token = models.CharField(max_length=250)
    refresh_token = models.CharField(max_length=200)
    token_uri = models.CharField(max_length=200)
    client_secret = models.CharField(max_length=200)
    create_date = models.DateTimeField('Create Date', auto_now_add=True)
    last_updated = models.DateTimeField('Last Updated', auto_now=True)

