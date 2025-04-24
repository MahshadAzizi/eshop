from django.db import models


class Product(models.Model):
    name = models.CharField(
        max_length=255,
        db_index=True
    )

    description = models.TextField(
        blank=True,
    )

    inventory = models.PositiveIntegerField()

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

    def __str__(self):
        return self.name
