from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import JsonResponse
from invoice.models import Invoice, Part, Labour
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import os
import stripe


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
    """A view to return stripe embeded form"""

    invoice = get_object_or_404(Invoice, slug=slug)

    checkout_url = reverse('create_checkout_session', kwargs={'slug': invoice.slug})
    
    template = 'checkout/payment.html'

    context = {
        'item': invoice,
        'checkout_url': checkout_url,
    }

    return render(request, template, context)


# STRIPE 
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
    'name': 'For Invoice: '+invoice.inv_number,
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
            metadata={
                'invoice_id':invoice.id
            },
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
        status = session.get('status')
        customer_email = session.get('customer_details', {}).get('email')

        return JsonResponse({'status': status, 'customer_email': customer_email})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def checkout_return(request):
    # Get session info 
    session_id = request.GET.get('session_id')
    session = stripe.checkout.Session.retrieve(session_id)

    # Get status and invoice
    status = session.get('status')
    inv_id = session.get('metadata', {}).get('invoice_id')
    invoice = get_object_or_404(Invoice, pk=inv_id)

    if status == 'complete' and invoice.status == 5:
        # Send confirmation email
        customer_email = session.get('customer_details', {}).get('email')
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'invoice': invoice, 'customer_email': customer_email}
        )
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'invoice': invoice, 'contact_email': settings.DEFAULT_FROM_EMAIL}
        )
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [customer_email]
        )
        # Change invoice status to complete
        invoice.status = 6
        invoice.save()
        
    session_status_url = reverse('session_status')

    context = {
        'session_status_url': session_status_url
    }
    return render(request, 'checkout/return.html', context)