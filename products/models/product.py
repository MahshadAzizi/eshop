from django.db import models


class Product(models.Model):
    name = models.CharField(
        max_length=255,
        db_index=True
    )

    description = models.TextField(
        blank=True,
    )

    inventory = models.PositiveIntegerField(
        default=0,
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['is_active']),
        ]

    def reduce_inventory(self, quantity: int):
        """Reduce the product's inventory by the given quantity."""
        self.inventory -= quantity
        self.save()

    def restore_inventory(self, quantity: int):
        """Restore the product's inventory by the given quantity."""
        self.inventory += quantity
        self.save()

    def product_deactivated(self):
        self.is_active = False
        self.save()

    def product_activate(self):
        self.is_active = True
        self.save()

    def __str__(self):
        return self.name
