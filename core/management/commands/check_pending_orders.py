from django.core.management.base import BaseCommand
from core.models import Order

class Command(BaseCommand):
    help = 'Checks for pending orders and sends a notification to Discord.'

    def handle(self, *args, **options):
        pending_orders = Order.objects.filter(paid=False)
        if pending_orders.exists():
            self.stdout.write(self.style.SUCCESS('Pending orders found.'))
            for order in pending_orders:
                self.stdout.write(f'Order ID: {order.id}, Total: ${order.get_total_cost()}')
        else:
            self.stdout.write(self.style.SUCCESS('No pending orders found.'))
