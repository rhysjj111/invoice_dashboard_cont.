from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import JsonResponse
from invoice.models import Invoice, Part, Labour
from django.conf import settings
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import os
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

def get_domain(request):
    if 'DYNO' in os.environ:  # Running on Heroku
        return 'https://' + settings.ALLOWED_HOSTS[0]
    else:  # Running locally
        return 'https://' + settings.ALLOWED_HOSTS[1]

@csrf_exempt
def create_checkout_session(request, slug):
    YOUR_DOMAIN = get_domain(request)
    
    invoice = get_object_or_404(Invoice, slug=slug)
    price = stripe.Price.create(
    unit_amount=invoice.grand_total,
    currency='gbp',
    product_data={
    'name': 'Custom Product',  # You can customize this name as needed
    # You can include more details about the product if necessary
    })
    
    if invoice:
        line_items = [{
            'price': price.id,
            'quantity': 1,
 
        }]
    else:
        return JsonResponse({'error': f'Invoice not found'}, status=404)
    
    try:
        session = stripe.checkout.Session.create(
            ui_mode = 'embedded',
            line_items=line_items,
            mode='payment',
            # success_url=YOUR_DOMAIN + reverse('checkout_success') + '?session_id={CHECKOUT_SESSION_ID}',
            # cancel_url=YOUR_DOMAIN + reverse('checkout_cancel'),
            return_url=YOUR_DOMAIN + reverse('checkout_return') + '?session_id={CHECKOUT_SESSION_ID}',
        )
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=403)

    return JsonResponse({'clientSecret': session.client_secret})

@csrf_exempt
def session_status(request):
    session_id = request.GET.get('session_id')
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        print(session, '***************************')
        status = session.get('status')
        print(status)
        customer_email = session.get('customer_details', {}).get('email')
        print(customer_email, '**************************************')
        return JsonResponse({'status': status, 'customer_email': customer_email})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def checkout_return(request):
    session_status_url = reverse('session_status')
    context = {
        'session_status_url': session_status_url
    }
    return render(request, 'checkout/return.html', context)

def checkout_cancel(request):
    return render(request, 'checkout/return.html')

def checkout_success(request):
    return render(request, 'checkout/return.html')





def landing_page(request, slug):
    """A view to return the landing page for customer payment"""
    invoice = get_object_or_404(Invoice, slug=slug)
    parts = Part.objects.filter(invoice=invoice.id)
    labour = Labour.objects.filter(invoice=invoice.id)

    template = 'checkout/landing_page.html'

    context = {
        'item': invoice,
        'parts_list': parts,
        'labour_list': labour,
    }

    return render(request, template, context)


def payment(request, slug):
    """A view to return checkout page"""

    invoice = get_object_or_404(Invoice, slug=slug)

    

    checkout_url = reverse('create_checkout_session', kwargs={'slug': invoice.slug})
    
    template = 'checkout/payment.html'

    context = {
        'item': invoice,
        'checkout_url': checkout_url,
    }

    return render(request, template, context)










# def customer_list(request):
#     """A view to return customer list with possible filter"""
#     customers = Customer.objects.filter(active=True)
#     customer_form = CustomerForm()
#     previous_url = 'customer_list'

#     template = 'customer/customer_list.html'
#     context = {
#         'customer_list': customers,
#         'customer_form': customer_form,
#         'previous_url': 'customer_list',
#     }
#     return render(request, template, context)


# def customer_summary(request, slug):
#     """A view to return a single-customer view"""
#     customer = get_object_or_404(Customer, slug=slug)
#     customer_form = CustomerForm(instance=customer)
#     previous_url = 'customer_list'

#     vehicles = Vehicle.objects.filter(customer=customer.id)
#     edit_vehicle_form_list = [
#         VehicleForm(instance=vehicle) for vehicle in vehicles]    
#     add_vehicle_form = VehicleForm(initial={'customer': customer.id})

#     context = {
#         'item': customer,
#         'previous_url': 'customer_list',
#         'add_vehicle_form': add_vehicle_form,
#         'edit_vehicle_form_list': edit_vehicle_form_list,
#         'vehicles': vehicles,
#         'customer_form': customer_form
#     }
#     return render(request, 'customer/customer_summary.html', context)

# # ---------------------------------------------------- CRUD CUSTOMER 
# def add_customer(request):
#     form = CustomerForm(request.POST, request.FILES)
#     if form.is_valid():
#         customer = form.save()
#         messages.success(request, f'Successfully added {customer.name}')
#         return redirect(reverse('customer_summary', args=[customer.slug]))
#     else:
#         messages.error(request, 'Failed to add customer. Please ensure the form is valid.')
#         return redirect(reverse('customer_list')) 

# def edit_customer(request, slug):
#     customer = get_object_or_404(Customer, slug=slug)
#     form = CustomerForm(request.POST, request.FILES, instance=customer)
#     if form.is_valid():
#         form.save()
#         messages.success(request, f'Successfully edited {customer.name}')
#         return redirect(reverse('customer_summary', args=[customer.slug]))
#     else:
#         messages.error(request, 'Failed to edit customer. Please ensure the form is valid.')
#         return redirect(reverse('customer_list')) 

# def delete_customer(request, slug):
#     customer = get_object_or_404(Customer, slug=slug)
#     customer.delete()
#     messages.success(request, f'Successfully deleted {customer.name}')
#     return redirect(reverse('customer_list'))

# # --------------------------------------------------------CRUD VEHICLE
# def add_vehicle(request): 
#     form = VehicleForm(request.POST, request.FILES)
#     if form.is_valid():
#         vehicle = form.save()
#         messages.success(request, f'Successfully added {vehicle.registration}')
#         return redirect(reverse('customer_summary', args=[vehicle.customer.slug]))
#     else:
#         messages.error(request, 'Failed to add customer. Please ensure the form is valid.')
#         return redirect(reverse('customer_summary')) #REDIRECT TO MAIN SCREEN TO AVOID NOTIFICATION AND MODAL ISSUE

# def edit_vehicle(request, slug):
#     vehicle = get_object_or_404(Vehicle, slug=slug)
#     form = VehicleForm(request.POST, request.FILES, instance=vehicle)
#     if form.is_valid():
#         form.save()
#         messages.success(request, f'Successfully edited {vehicle.registration}')
#         return redirect(reverse('customer_summary', args=[vehicle.customer.slug]))
#     else:
#         messages.error(request, 'Failed to add customer. Please ensure the form is valid.')
#         return redirect(reverse('customer_summary')) #REDIRECT TO MAIN SCREEN TO AVOID NOTIFICATION AND MODAL ISSUE

# def delete_vehicle(request, slug):
#     vehicle = get_object_or_404(Vehicle, slug=slug)
#     vehicle.delete()
#     messages.success(request, f'Successfully deleted {vehicle.registration}')
#     return redirect(reverse('customer_summary', args=[vehicle.customer.slug]))


        



