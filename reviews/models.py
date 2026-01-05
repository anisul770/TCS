from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from services.models import Service
from users.models import User

# Create your models here.
class Review(models.Model):
    service = models.ForeignKey(Service,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['service','user']
    
    def __str__(self):
        return f"Review by {self.user.first_name} on {self.service.name}"
    
    