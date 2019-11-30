from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE )
    full_name = models.CharField(max_length=40, blank=False)
    codeforces_id = models.CharField(max_length=40, blank=False)
    Uva_Id = models.CharField(max_length=40, blank=False)
    points= models.IntegerField(default = 0 , blank= True)
    department = models.CharField(max_length= 40,blank= False)
    red_mark = models.BooleanField(default=False)
    TotalContest= models.IntegerField(default=0)
    TotalSolve = models.IntegerField(default= 0)

    def __str__(self):
        return self.full_name