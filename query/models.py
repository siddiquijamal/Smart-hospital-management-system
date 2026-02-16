from django.db import models

# Create your models here.


class Query(models.Model):
    
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    query = models.TextField(max_length=1000)
    
    
    def __str__(self):
        return self.name
    