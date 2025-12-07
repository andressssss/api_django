from django.db import models
from .cliente import Cliente


class Deuda(models.Model):
    ESTADOS = (
        ("pendiente", "Pendiente"),
        ("pagada", "Pagada"),
        ("vencida", "Vencida"),
    )

    cliente = models.ForeignKey(
        Cliente, related_name="deudas", on_delete=models.CASCADE
    )
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="pendiente")
    vencimiento = models.DateField()
    tipo = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
