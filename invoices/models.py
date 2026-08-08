from datetime import timedelta
from django.db import models
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal


# =========================================================
# CUSTOMER
# =========================================================

class Customer(models.Model):

    name = models.CharField(
        max_length=200
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    address = models.TextField(
        blank=True,
        null=True
    )

    gst_number = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


# =========================================================
# INVOICE
# =========================================================

class Invoice(models.Model):

    STATUS_CHOICES = [
        ('UNPAID', 'Unpaid'),
        ('PAID', 'Paid'),
        ('CANCELLED', 'Cancelled'),
    ]

    # -----------------------------------------------------
    # Invoice Number
    # Example:
    # QK-2026-0001
    # QK-2026-0002
    # -----------------------------------------------------

    invoice_number = models.CharField(
        max_length=30,
        unique=True,
        blank=True
    )

    # -----------------------------------------------------
    # Customer
    # -----------------------------------------------------

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name='invoices'
    )

    # -----------------------------------------------------
    # Dates
    # -----------------------------------------------------

    invoice_date = models.DateField(
        default=timezone.localdate
    )

    due_date = models.DateField(
        blank=True,
        null=True
    )

    # -----------------------------------------------------
    # GST
    # -----------------------------------------------------

    gst_rate = models.DecimalField(
    max_digits=5,
    decimal_places=2,
    default= Decimal("18.00")
)

    # -----------------------------------------------------
    # Amounts
    # -----------------------------------------------------

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    gst_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    # -----------------------------------------------------
    # Status
    # -----------------------------------------------------

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='UNPAID'
    )

    # -----------------------------------------------------
    # Notes
    # -----------------------------------------------------

    notes = models.TextField(
        blank=True,
        null=True
    )

    # -----------------------------------------------------
    # Created timestamp
    # -----------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # =====================================================
    # GENERATE INVOICE NUMBER
    # =====================================================

    def generate_invoice_number(self):

        year = self.invoice_date.year

        last_invoice = (
            Invoice.objects
            .filter(
                invoice_number__startswith=f"QK-{year}-"
            )
            .order_by('-id')
            .first()
        )

        if last_invoice:

            last_number = int(
                last_invoice.invoice_number.split('-')[-1]
            )

            next_number = last_number + 1

        else:

            next_number = 1

        return f"QK-{year}-{next_number:04d}"

    # =====================================================
    # SAVE
    # =====================================================

    def save(self, *args, **kwargs):

        # -----------------------------------------------
        # Generate Invoice Number
        # -----------------------------------------------

        if not self.invoice_number:

            self.invoice_number = (
                self.generate_invoice_number()
            )

        # -----------------------------------------------
        # Due Date = Invoice Date + 3 Days
        # -----------------------------------------------

        if self.invoice_date:

            self.due_date = (
                self.invoice_date
                + timedelta(days=3)
            )

        super().save(*args, **kwargs)

    # =====================================================
    # STRING REPRESENTATION
    # =====================================================

    def __str__(self):

        return (
            self.invoice_number
            or "New Invoice"
        )


# =========================================================
# INVOICE ITEM
# =========================================================

class InvoiceItem(models.Model):

    # -----------------------------------------------------
    # Invoice Relationship
    # -----------------------------------------------------

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='items'
    )

    # -----------------------------------------------------
    # Description
    # -----------------------------------------------------

    description = models.CharField(
        max_length=500
    )

    # -----------------------------------------------------
    # Quantity
    # -----------------------------------------------------

    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1
    )

    # -----------------------------------------------------
    # Rate
    # -----------------------------------------------------

    rate = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    # -----------------------------------------------------
    # Amount
    # -----------------------------------------------------

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    # =====================================================
    # SAVE ITEM
    # =====================================================

    def save(self, *args, **kwargs):

        # Amount = Quantity × Rate

        self.amount = (
            self.quantity * self.rate
        )

        super().save(*args, **kwargs)

    # =====================================================
    # STRING REPRESENTATION
    # =====================================================

    def __str__(self):

        return self.description