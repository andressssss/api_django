from rest_framework import viewsets
from clients.models.deuda import Deuda
from clients.serializers.deuda import DeudaSerializer

class DeudaViewSet(viewsets.ModelViewSet):
    queryset = Deuda.objects.all()
    serializer_class = DeudaSerializer
