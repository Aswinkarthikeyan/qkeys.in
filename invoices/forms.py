from django import forms

from .models import Invoice


class InvoiceForm(forms.ModelForm):

    class Meta:
        model = Invoice

        fields = [
            'customer',
            'invoice_date',
            'notes',
        ]

        widgets = {

            'invoice_date': forms.DateInput(
                attrs={
                    'type': 'date'
                }
            ),

            'notes': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': 'Additional notes...'
                }
            ),
        }
        
    from decimal import Decimal

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.http import HttpResponse

from django.template.loader import render_to_string

from django.utils import timezone

from .models import Invoice, InvoiceItem
from .forms import InvoiceForm
from decimal import Decimal

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
            # Item details from form
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
            # Validate item
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

                quantity = Decimal(quantity)

                rate = Decimal(rate)


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
                    item.amount
                    for item in items
                )


                # -----------------------------
                # GST 18%
                # -----------------------------

                gst_rate = Decimal(
                    '18.00'
                )

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
                # Save totals
                # -----------------------------

                invoice.gst_rate = gst_rate

                invoice.subtotal = subtotal

                invoice.gst_amount = gst_amount

                invoice.total_amount = total_amount

                invoice.save()


                # -----------------------------
                # Go to preview
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