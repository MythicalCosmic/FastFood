from django.db import models
from safedelete.config import SOFT_DELETE



class Size(models.Model):
    name = models.CharField(max_length=50)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Ingridients(models.Model):
    size_id = models.ForeignKey(Size, on_delete=models.RESTRICT)
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    expiration_data = models.DateField()


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

