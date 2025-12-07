from rest_framework import viewsets
from clients.models.portafolio import Portafolio
from clients.serializers.portafolio import PortafolioSerializer

class PortafolioViewSet(viewsets.ModelViewSet):
    queryset = Portafolio.objects.all()
    serializer_class = PortafolioSerializer
