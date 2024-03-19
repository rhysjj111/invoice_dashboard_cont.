from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Customer
from .forms import CustomerForm
from django.contrib import messages

def customer_list(request):
    """A view to return main customer view"""

    customers = Customer.objects.filter(active=True)

    form = CustomerForm()

    previous_url = 'customer_list'
    delete_url = 'customer_list'

    template = 'customer/customer_list.html'
    context = {
        'customer_list': customers,
        'form': form,
        'previous_url': 'customer_list',
        'delete_url': delete_url,
    }
    return render(request, template, context)

def add_customer(request):
    form = CustomerForm(request.POST, request.FILES)
    if form.is_valid():
        customer = form.save()
        messages.success(request, 'Successfully added customer!')
        return redirect(reverse('customer_summary', args=[customer.id]))
    else:
        messages.error(request, 'Failed to add customer. Please ensure the form is valid.')
        return redirect(reverse('customer_summary'+'#open_modal')) #maybe work?


def customer_summary(request):
    """A view to return a single-customer view"""
    previous_url = 'customer_list'
    delete_url = 'customer_list'
    context = {
        'previous_url': 'customer_list',
        'delete_url': delete_url,
    }
    return render(request, 'customer/customer_summary.html', context)
