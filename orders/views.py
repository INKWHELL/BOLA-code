from rest_framework import generics, permissions

from .models import Order
from .serializers import OrderSerializer


class OrderDetailVulnerable(generics.RetrieveAPIView):
    """
    VULNERABLE: checks that the caller is authenticated, but the
    queryset is not scoped to the caller. Any authenticated user can
    retrieve any order by ID. This is BOLA (OWASP API1:2023).
    """
    queryset = Order.objects.all()          # <-- not filtered by owner
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]


class OrderDetailFixed(generics.RetrieveAPIView):
    """
    FIXED: the queryset is scoped to request.user before the lookup
    is applied, so an object not owned by the caller is not present
    in the queryset at all (404, not 403 or 200).
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(owner=self.request.user)
