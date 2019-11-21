from django.db import models

# Create your models here.

class Users(models.Model):
    firstName=models.CharField(max_length=40)
    lastName=models.CharField(max_length=40)
    email=models.CharField(max_length=40, unique=True)
    userName = models.CharField(max_length=40)
    phone = models.CharField(max_length=40)
    codeforcesHandle = models.CharField(max_length=40)
    uvaHandle = models.CharField(max_length=40)
    lightOJ = models.CharField(max_length=40)
    password=models.CharField(max_length=40)

    def __str__(self):
        return self.userName
