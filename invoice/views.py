from django.shortcuts import render, redirect, reverse, get_object_or_404
from .forms import InvoiceForm
from .models import Invoice, Part, Labour
from django.contrib import messages



def extract_options(status_options, *keys_to_keep):
    """Extracts keys and values from dictionary"""
    return {key: status_options[key] for key in keys_to_keep}





def invoice_list(request):
    """A view to return main invoice view"""
    if request.POST:
        invoice_pk = request.POST.get('pk')
        invoice_status = int(request.POST.get('status'))
        invoice = get_object_or_404(Invoice, pk=invoice_pk)
        invoice.status = invoice_status
        invoice.save()        
        messages.success(request, f'Successfully')
        return redirect(reverse('invoice_list'))
    else:
        create_invoice_form = InvoiceForm(initial={'status': 2})
        invoices = Invoice.objects.all()
        all_status_options = dict(Invoice.InvoiceStatus.choices)
        
        status_mapping = {
            1: (2, 2),
            2: (3, 1),
            3: (4, 2),
            4: (5, 3),
            5: (6, 4)
        }
        for invoice in invoices:
            available_status_options = status_mapping.get(invoice.status, {})
            invoice.available_status_options = extract_options(all_status_options, *available_status_options)
            

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


def invoice_summary(request, slug):
    """A view to return a single-invoice view"""
    invoice = get_object_or_404(Invoice, slug=slug)
    previous_url = 'invoice_list'
    delete_url = 'invoice_list'
    context = {
        'item': invoice,
        'previous_url': 'invoice_list',
        'delete_url': delete_url,
    }
    return render(request, 'invoice/invoice_summary.html', context)
