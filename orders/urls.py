from django.urls import path

from .views import OrderDetailFixed, OrderDetailVulnerable

urlpatterns = [
    path("vuln/orders/<int:pk>/", OrderDetailVulnerable.as_view(), name="order-vuln"),
    path("orders/<int:pk>/", OrderDetailFixed.as_view(), name="order-fixed"),
]
