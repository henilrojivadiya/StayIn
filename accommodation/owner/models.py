from django.db import models

# Create your models here.

class Owner(models.Model):
    firstName           = models.CharField(max_length=200)
    lastName            = models.CharField(max_length=200)
    email               = models.EmailField(max_length=200, unique=True)
    address             = models.CharField(max_length=500)
    phoneNumber         = models.CharField(max_length=10, unique=True)

    class Meta:
        verbose_name = ("Owner")
        verbose_name_plural = ("Owners")
    
    def __str__(self):
        return self.firstName + ' ' + self.lastName + ' (' + str(self.id) + ')'
