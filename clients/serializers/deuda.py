from rest_framework import serializers

from clients.models.deuda import Deuda


class DeudaSerializer(serializers.ModelSerializer):
    cliente = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Deuda
        fields = "__all__"
