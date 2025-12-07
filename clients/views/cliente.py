from clients.models.cliente import Cliente
from clients.serializers.cliente import ClienteSerializer
from clients.serializers.portafolio import PortafolioSerializer
from clients.serializers.deuda import DeudaSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all().order_by("-id")
    serializer_class = ClienteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["zona", "documento"]

    def get_queryset(self):
        queryset = super().get_queryset()
        ids = self.request.query_params.get('ids')
        if ids:
            id_list = [int(i) for i in ids.split(',')]
            queryset = queryset.filter(id__in=id_list)
        return queryset

    @action(detail=True, methods=['get'])
    def portafolios(self, request, pk=None):
        cliente = self.get_object()
        portafolios = cliente.portafolios.all()
        serializer = PortafolioSerializer(portafolios, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get', 'post'])
    def deudas(self, request, pk=None):
        cliente = self.get_object()
        if request.method == 'POST':
            serializer = DeudaSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(cliente=cliente)
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        else:
            deudas = cliente.deudas.all()
            serializer = DeudaSerializer(deudas, many=True)
            return Response(serializer.data)
