from django.urls import path
from . import views

app_name = 'invoices'

urlpatterns = [

    path(
        'create/',
        views.create_invoice,
        name='create_invoice'
    ),

    path(
        '<int:invoice_id>/preview/',
        views.invoice_preview,
        name='invoice_preview'
    ),

    path(
        '<int:invoice_id>/pdf/',
        views.invoice_pdf,
        name='invoice_pdf'
    ),

    path(
        '<int:invoice_id>/download/',
        views.invoice_download,
        name='invoice_download'
    ),
]