from rest_framework import serializers

from clients.models.portafolio import Portafolio


class PortafolioSerializer(serializers.ModelSerializer):
    cliente = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Portafolio
        fields = "__all__"
