from django.conf import settings
from django.db import models


class Order(models.Model):
    """A single order record, owned by exactly one user."""
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.CharField(max_length=200)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.id} ({self.owner.username}): {self.item}"
