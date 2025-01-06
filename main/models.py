from django.db import models
from safedelete.config import SOFT_DELETE
from django.contrib.auth.models import User


class Size(models.Model):
    _safedelete_policy = SOFT_DELETE
    name = models.CharField(max_length=50)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Ingridients(models.Model):
    _safedelete_policy = SOFT_DELETE
    size_id = models.ForeignKey(Size, on_delete=models.RESTRICT)
    name = models.CharField(max_length=100)
    expiration_data = models.DateField()


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class IngridientInvoice(models.Model):
    _safedelete_policy = SOFT_DELETE
    name = models.CharField(max_length=50)
    status = models.CharField(max_length=10, choices=[('draft', 'Draft'), ('accepted', 'Accepted'), ('canceled', 'Canceled')], default='draft')
    user = models.ForeignKey(User, on_delete=models.RESTRICT)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Invoice {self.id} - {self.status}"
    

class IngridientInvoiceItem(models.Model):
    _safedelete_policy = SOFT_DELETE
    igridient_invoice = models.ForeignKey(IngridientInvoice, on_delete=models.RESTRICT)
    ingridient = models.ForeignKey(Ingridients, on_delete=models.RESTRICT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Stock(models.Model):
    _safedelete_policy = SOFT_DELETE
    ingridient = models.ForeignKey(Ingridients, on_delete=models.RESTRICT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)



    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.ingridient} - {self.quantity} items"



class StockMovement(models.Model):
    _safedelete_policy = SOFT_DELETE
    MOVEMENT_TYPES = [('arrival', 'Arrival'), ('departure', 'Departure')]


    ingridient = models.ForeignKey(Ingridients, on_delete=models.RESTRICT)
    type = models.CharField(max_length=10, choices=MOVEMENT_TYPES)
    quantity = models.PositiveIntegerField()
    description = models.TextField(blank=True)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.type.capitalize()} - {self.variant} ({self.quantity})"