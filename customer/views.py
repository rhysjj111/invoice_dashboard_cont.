from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Customer, Vehicle
from .forms import CustomerForm, VehicleForm
from django.contrib import messages

def customer_list(request):
    """A view to return customer list with possible filter"""
    customers = Customer.objects.filter(active=True)
    customer_form = CustomerForm()
    previous_url = 'customer_list'

    template = 'customer/customer_list.html'
    context = {
        'customer_list': customers,
        'customer_form': customer_form,
        'previous_url': 'customer_list',
    }
    return render(request, template, context)


def customer_summary(request, slug):
    """A view to return a single-customer view"""
    customer = get_object_or_404(Customer, slug=slug)
    customer_form = CustomerForm(instance=customer)
    previous_url = 'customer_list'

    vehicles = Vehicle.objects.filter(customer=customer.id)
    edit_vehicle_form_list = [
        VehicleForm(instance=vehicle) for vehicle in vehicles]    
    add_vehicle_form = VehicleForm(initial={'customer': customer.id})

    context = {
        'item': customer,
        'previous_url': 'customer_list',
        'add_vehicle_form': add_vehicle_form,
        'edit_vehicle_form_list': edit_vehicle_form_list,
        'vehicles': vehicles,
        'customer_form': customer_form
    }
    return render(request, 'customer/customer_summary.html', context)

# ---------------------------------------------------- CRUD CUSTOMER 
def add_customer(request):
    form = CustomerForm(request.POST, request.FILES)
    if form.is_valid():
        customer = form.save()
        messages.success(request, f'Successfully added {customer.name}')
        return redirect(reverse('customer_summary', args=[customer.slug]))
    else:
        messages.error(request, 'Failed to add customer. Please ensure the form is valid.')
        return redirect(reverse('customer_list')) 

def edit_customer(request, slug):
    customer = get_object_or_404(Customer, slug=slug)
    form = CustomerForm(request.POST, request.FILES, instance=customer)
    if form.is_valid():
        form.save()
        messages.success(request, f'Successfully edited {customer.name}')
        return redirect(reverse('customer_summary', args=[customer.slug]))
    else:
        messages.error(request, 'Failed to edit customer. Please ensure the form is valid.')
        return redirect(reverse('customer_list')) 

def delete_customer(request, slug):
    customer = get_object_or_404(Customer, slug=slug)
    customer.delete()
    messages.success(request, f'Successfully deleted {customer.name}')
    return redirect(reverse('customer_list'))

# --------------------------------------------------------CRUD VEHICLE
def add_vehicle(request): 
    form = VehicleForm(request.POST, request.FILES)
    if form.is_valid():
        vehicle = form.save()
        messages.success(request, f'Successfully added {vehicle.registration}')
        return redirect(reverse('customer_summary', args=[vehicle.customer.slug]))
    else:
        messages.error(request, 'Failed to add customer. Please ensure the form is valid.')
        return redirect(reverse('customer_summary')) #REDIRECT TO MAIN SCREEN TO AVOID NOTIFICATION AND MODAL ISSUE

def edit_vehicle(request, slug):
    vehicle = get_object_or_404(Vehicle, slug=slug)
    form = VehicleForm(request.POST, request.FILES, instance=vehicle)
    if form.is_valid():
        form.save()
        messages.success(request, f'Successfully edited {vehicle.registration}')
        return redirect(reverse('customer_summary', args=[vehicle.customer.slug]))
    else:
        messages.error(request, 'Failed to add customer. Please ensure the form is valid.')
        return redirect(reverse('customer_summary')) #REDIRECT TO MAIN SCREEN TO AVOID NOTIFICATION AND MODAL ISSUE

def delete_vehicle(request, slug):
    vehicle = get_object_or_404(Vehicle, slug=slug)
    vehicle.delete()
    messages.success(request, f'Successfully deleted {vehicle.registration}')
    return redirect(reverse('customer_summary', args=[vehicle.customer.slug]))


        



