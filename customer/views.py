from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Customer
from .forms import CustomerForm
from django.contrib import messages

def customer_list(request):
    """A view to return customer list with possible filter"""
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


def customer_summary(request, slug):
    """A view to return a single-customer view"""
    customer = get_object_or_404(Customer, slug=slug)
    form = CustomerForm(instance=customer)
    previous_url = 'customer_list'
    delete_url = 'customer_list'
    context = {
        'instance': customer,
        'previous_url': 'customer_list',
        'form': form
    }
    return render(request, 'customer/customer_summary.html', context)
    

def add_customer(request):
    form = CustomerForm(request.POST, request.FILES)
    if form.is_valid():
        customer = form.save()
        messages.success(request, 'Successfully added {customer.friendly_name}!')
        return redirect(reverse('customer_summary', args=[customer.slug]))
    else:
        messages.error(request, 'Failed to add customer. Please ensure the form is valid.')
        return redirect(reverse('customer_summary'+'#open_modal')) #maybe work?

def edit_customer(request, slug):
    customer = get_object_or_404(Customer, slug=slug)
    form = CustomerForm(request.POST, request.FILES, instance=customer)
    if form.is_valid():
        form.save()
        messages.success(request, 'Successfully edited {customer.friendly_name}!')
        return redirect(reverse('customer_summary', args=[customer.slug]))

def delete_customer(request, slug):
    customer = get_object_or_404(Customer, slug=slug)
    customer.delete()
    messages.success(request, 'Customer deleted')
    return redirect(reverse('customer_list'))

        



