"""
Serializers for graphic APIs
"""
from rest_framework import serializers

from core.models import (
    Graphic,
)

class GraphicSerializer(serializers.ModelSerializer):
    """Serializer for graphics."""

    class Meta:
        model = Graphic
        fields = [
            "id",
            "image"
        ]
        read_only_fields = ["id"]
        extra_kwargs = {"image": {"required": "True"}}

    def create(self, validated_data):
        """Create a graphic."""
        graphic = Graphic.objects.create(**validated_data)

        return graphic