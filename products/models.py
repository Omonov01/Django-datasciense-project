from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=220)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.name)
    

class Purchase(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    total_price = models.PositiveIntegerField(blank=True)
    salesman = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    def save(self,*args, **kwargs):
        self.total_price = self.price * self.quantity
        if not self.date:
            self.date = datetime.now()
        super(Purchase, self).save(*args, **kwargs)
        super().save(*args, **kwargs)
    
    # def saves(self, *args, **kwargs):
    #     if not self.date:
    #         self.date = datetime.now()
    #     super(Purchase, self).save(*args, **kwargs)
 
    def __str__(self) -> str:
        return "{} dona - {} maxsuloti {} so'mdan sotildi.Jami  summa {}.".format(self.quantity, self.product.name, self.price, self.total_price)