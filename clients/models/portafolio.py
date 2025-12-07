from django.db import models

from .cliente import Cliente


class Portafolio(models.Model):
    cliente = models.ForeignKey(
        Cliente, related_name="portafolios", on_delete=models.CASCADE
    )
    tipo = models.CharField(max_length=50)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    datos = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)
