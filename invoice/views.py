from django.shortcuts import render

def index(request):
    """A view to return main invoice view"""
    previous_url = 'invoice_list'
    delete_url = 'invoice_list'
    context = {
  
        'delete_url': delete_url
    }
    return render(request, 'invoice/index.html', context)
