from django.contrib import admin

from .models import (
    Customer,
    Invoice,
    InvoiceItem
)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'phone',
        'email',
        'gst_number',
        'created_at',
    )

    search_fields = (
        'name',
        'phone',
        'email',
        'gst_number',
    )


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):

    list_display = (
        'invoice_number',
        'customer',
        'invoice_date',
        'due_date',
        'subtotal',
        'gst_amount',
        'total_amount',
        'status',
    )

    search_fields = (
        'invoice_number',
        'customer__name',
    )

    list_filter = (
        'status',
        'invoice_date',
    )


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):

    list_display = (
        'invoice',
        'description',
        'quantity',
        'rate',
        'amount',
    )

    search_fields = (
        'description',
        'invoice__invoice_number',
    )