from rest_framework import serializers
from clients.models.deuda import Deuda


class DeudaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deuda
        fields = "__all__"
