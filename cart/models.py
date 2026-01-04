from django.db import models
from uuid import uuid4
from users.models import User
from services.models import Service

# Create your models here.

class Cart(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid4,editable=False)
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Cart of {self.user.first_name}"
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cart')
    service = models.ForeignKey(Service,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    
    class Meta:
        unique_together = [['cart','service']]

    def __str__(self):
        return f"{self.quantity} x {self.service.name}"
    

