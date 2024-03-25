from django.shortcuts import render
from .forms import InitiateInvoice

def invoice_list(request):
    """A view to return main invoice view"""
    create_invoice_form = InitiateInvoice()
    context = {
        'create_invoice_form': create_invoice_form
    }
    return render(request, 'invoice/invoice_list.html', context)


def invoice_summary(request):
    """A view to return a single-invoice view"""
    previous_url = 'invoice_list'
    delete_url = 'invoice_list'
    context = {
        'previous_url': 'invoice_list',
        'delete_url': delete_url,
    }
    return render(request, 'invoice/invoice_summary.html', context)
