from django.shortcuts import render, redirect, reverse, get_object_or_404
from .forms import InvoiceForm
from .models import Invoice, Part, Labour
from django.contrib import messages

def invoice_list(request):
    """A view to return main invoice view"""
    create_invoice_form = InvoiceForm()
    invoices = Invoice.objects.all()
    context = {
        'create_invoice_form': create_invoice_form,
        'invoices': invoices
    }
    return render(request, 'invoice/invoice_list.html', context)

def create_invoice(request):
    form = InvoiceForm(request.POST, request.FILES)
    if form.is_valid():
        invoice = form.save()
        messages.success(request, f'Successfully added invoice')
        return redirect(reverse('invoice', args=[invoice.slug]))
    else:
        messages.error(request, 'Failed to add invoice. Please ensure the form is valid.')
        return redirect(reverse('invoice_list')) 


def invoice_summary(request):
    """A view to return a single-invoice view"""
    previous_url = 'invoice_list'
    delete_url = 'invoice_list'
    context = {
        'previous_url': 'invoice_list',
        'delete_url': delete_url,
    }
    return render(request, 'invoice/invoice_summary.html', context)
