from django.shortcuts import render

def index(request):
    """A view to return main invoice view"""
    return render(request, 'invoice/index.html')
