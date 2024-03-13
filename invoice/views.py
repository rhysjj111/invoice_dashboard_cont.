from django.shortcuts import render

def invoice_list(request):
    """A view to return main invoice view"""
    previous_url = 'invoice_list'
    delete_url = 'invoice_list'
    context = {
        'previous_url': 'invoice_list',
        'delete_url': delete_url,
    }
    return render(request, 'invoice/invoice_list.html', context)


def invoice(request):
    """A view to return a single-invoice view"""
    previous_url = 'invoice_list'
    delete_url = 'invoice_list'
    context = {
        'previous_url': 'invoice_list',
        'delete_url': delete_url,
    }
    return render(request, 'invoice/invoice.html', context)
