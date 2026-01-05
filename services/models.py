from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    
    def __str__(self):
        return self.name
    
class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=2) 
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='services')
    avg_rating = models.FloatField(max_length=2,validators=[MinValueValidator(0),MaxValueValidator(5)],default=0)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name