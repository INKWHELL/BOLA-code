from rest_framework import serializers

from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source="owner.username", read_only=True)

    class Meta:
        model = Order
        fields = ["id", "owner", "item", "total"]
