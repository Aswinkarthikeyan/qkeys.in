import os

os.add_dll_directory(
    r"C:\msys64\ucrt64\bin"
)
from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone

from .models import Invoice, InvoiceItem
from .forms import InvoiceForm

from properties.models import Property


def create_invoice(request):

    if request.method == 'POST':

        form = InvoiceForm(request.POST)

        if form.is_valid():

            # -----------------------------
            # Invoice details
            # -----------------------------

            customer = form.cleaned_data['customer']

            invoice_date = form.cleaned_data[
                'invoice_date'
            ]

            notes = form.cleaned_data['notes']


            # -----------------------------
            # Item details
            # -----------------------------

            description = request.POST.get(
                'description'
            )

            quantity = request.POST.get(
                'quantity'
            )

            rate = request.POST.get(
                'rate'
            )


            # -----------------------------
            # Validate item details
            # -----------------------------

            if not description:

                form.add_error(
                    None,
                    'Description is required.'
                )

            elif not quantity:

                form.add_error(
                    None,
                    'Quantity is required.'
                )

            elif not rate:

                form.add_error(
                    None,
                    'Rate is required.'
                )

            else:

                try:

                    quantity = Decimal(quantity)
                    rate = Decimal(rate)

                except:

                    form.add_error(
                        None,
                        'Quantity and Rate must be valid numbers.'
                    )

                else:

                    if quantity <= 0:

                        form.add_error(
                            None,
                            'Quantity must be greater than zero.'
                        )

                    elif rate < 0:

                        form.add_error(
                            None,
                            'Rate cannot be negative.'
                        )

                    else:

                        # -----------------------------
                        # Create Invoice
                        # -----------------------------

                        invoice = Invoice.objects.create(

                            customer=customer,

                            invoice_date=invoice_date,

                            notes=notes
                        )


                        # -----------------------------
                        # Create Invoice Item
                        # -----------------------------

                        InvoiceItem.objects.create(

                            invoice=invoice,

                            description=description,

                            quantity=quantity,

                            rate=rate
                        )


                        # -----------------------------
                        # Calculate subtotal
                        # -----------------------------

                        items = invoice.items.all()

                        subtotal = sum(
                            (
                                item.amount
                                for item in items
                            ),
                            Decimal('0.00')
                        )


                        # -----------------------------
                        # GST 18%
                        # -----------------------------

                        gst_rate = Decimal('18.00')

                        gst_amount = (
                            subtotal
                            * gst_rate
                            / Decimal('100')
                        )


                        # -----------------------------
                        # Total
                        # -----------------------------

                        total_amount = (
                            subtotal
                            + gst_amount
                        )


                        # -----------------------------
                        # Save invoice totals
                        # -----------------------------

                        invoice.gst_rate = gst_rate

                        invoice.subtotal = subtotal

                        invoice.gst_amount = gst_amount

                        invoice.total_amount = total_amount

                        invoice.save()


                        # -----------------------------
                        # Go to Preview
                        # -----------------------------

                        return redirect(
                            'invoices:invoice_preview',
                            invoice_id=invoice.id
                        )

    else:

        form = InvoiceForm(
            initial={
                'invoice_date':
                    timezone.localdate()
            }
        )


    return render(
        request,
        'invoices/create_invoice.html',
        {
            'form': form
        }
    )
    
        
def invoice_preview(request, invoice_id):

    invoice = get_object_or_404(
        Invoice,
        id=invoice_id
    )

    items = invoice.items.all()

    context = {
        'invoice': invoice,
        'items': items,
    }

    return render(
        request,
        'invoices/invoice_preview.html',
        context
    )
    
def invoice_pdf(request, invoice_id):

    invoice = get_object_or_404(
        Invoice,
        id=invoice_id
    )

    items = invoice.items.all()

    html_string = render_to_string(
        'invoices/invoice_pdf.html',
        {
            'invoice': invoice,
            'items': items,
        }
    )

    from weasyprint import HTML

    pdf_file = HTML(
        string=html_string,
        base_url=request.build_absolute_uri('/')
    ).write_pdf()

    response = HttpResponse(
        pdf_file,
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        f'inline; '
        f'filename="{invoice.invoice_number}.pdf"'
    )

    return response

def invoice_download(request, invoice_id):

    invoice = get_object_or_404(
        Invoice,
        id=invoice_id
    )

    items = invoice.items.all()

    html_string = render_to_string(
        'invoices/invoice_pdf.html',
        {
            'invoice': invoice,
            'items': items,
        }
    )

    from weasyprint import HTML

    pdf_file = HTML(
        string=html_string,
        base_url=request.build_absolute_uri('/')
    ).write_pdf()

    response = HttpResponse(
        pdf_file,
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        f'attachment; '
        f'filename="{invoice.invoice_number}.pdf"'
    )

    return response