from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from rest_framework.authtoken.models import Token

from orders.models import Order


class Command(BaseCommand):
    help = "Create two unprivileged test accounts, each owning one order."

    def handle(self, *args, **options):
        User.objects.filter(username__in=["user_a", "user_b"]).delete()

        user_a = User.objects.create_user(username="user_a", password="test1234")
        user_b = User.objects.create_user(username="user_b", password="test1234")

        token_a = Token.objects.create(user=user_a)
        token_b = Token.objects.create(user=user_b)

        order_a = Order.objects.create(owner=user_a, item="Widget", total="19.99")
        order_b = Order.objects.create(owner=user_b, item="Confidential Report", total="499.00")

        self.stdout.write(self.style.SUCCESS("Seed complete.\n"))
        self.stdout.write(f"User A  -> username=user_a  order_id={order_a.id}  token={token_a.key}")
        self.stdout.write(f"User B  -> username=user_b  order_id={order_b.id}  token={token_b.key}")
