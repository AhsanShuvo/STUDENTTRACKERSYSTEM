from django.db import models

# Create your models here.

class CONTEST(models.Model):
    number = models.IntegerField(blank= False)
    Name = models.CharField(max_length = 100, blank= False)
    user_id = models.CharField(max_length = 100, blank= False)
    solve = models.IntegerField(default=0)
    position=models.IntegerField(default=9999)

    def __str__(self):
        return self.Name

