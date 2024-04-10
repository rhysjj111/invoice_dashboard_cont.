from django.shortcuts import render, redirect, reverse, get_object_or_404
from .forms import InvoiceForm, PartFormSet, BasePartFormSetHelper, LabourFormSet, BaseLabourFormSetHelper
from .models import Invoice, Part, Labour
from django.contrib import messages
from django.db.models import Q
from django.db import transaction
from django.conf import settings
from invoice_dashboard.utils import user_group_contains

from invoice_dashboard.utils import get_domain

from django.core.mail import send_mail
from django.template.loader import render_to_string


# A map for avaiable invoice status option keys, depending on current status 
available_status_key_map = {
    1: (2,),
    2: (3, 1),
    3: (4, 2),
    4: (5, 3),
    5: (6,)
}

# All possible status options and their values
all_status_options_dict = dict(Invoice.InvoiceStatus.choices)
all_status_options_dict[5] = 'Send to customer'
all_status_options_dict[6] = 'Paid'

# A dictionary of dictionaries, where each original status maps it's available status' keys and values
available_status_full_dict_map = {
    key: {value: all_status_options_dict[value] for value in status_tuple} 
    for key, status_tuple in available_status_key_map.items()
} 

def invoice_list(request):
    """A view to return main invoice view"""
    create_invoice_form = InvoiceForm(initial={'status': 2})
    invoices = Invoice.objects.all()    

    query = None
    filter_mapping = {
        'active': [2, 3, 4],
        'pending': [5,],
        'inactive': [1, 6]
    }
    
    # if user_group_contains(request, 'Accounts'):
    #     filter = 'pending'
    # else:
    filter = 'active'

    if request.method == 'POST':
        filter = request.POST.get('filter')
        invoice_pk = request.POST.get('pk')
        # Get invoice
        invoice = get_object_or_404(Invoice, pk=invoice_pk)
        # Get new invoice status user has selected
        new_invoice_status = int(request.POST.get('status'))
        # Send invoice summary to customer if new status is 
        # 'send to customer'
        if new_invoice_status == 5:
            try:
                with transaction.atomic():
                    # Change invoice status      
                    invoice.status = new_invoice_status
                    invoice.save()
                    DOMAIN = get_domain(request)
                    landing_page = DOMAIN + reverse('landing_page', args=[invoice.slug])
                    subject = render_to_string(
                        'invoice/request_payment_email/request_payment_subject.txt',
                        {'invoice': invoice}
                    )
                    body = render_to_string(
                        'invoice/request_payment_email/request_payment_body.txt',
                        {'invoice': invoice, 'landing_page': landing_page}
                    )
                    send_mail(
                        subject,
                        body,
                        settings.DEFAULT_FROM_EMAIL,
                        [invoice.customer.email]
                    )
            except Exception as e:
                # If email failed then redirect with error message
                transaction.rollback()
                messages.error(
                    request, f'Invoice failed to send to customer. Check email '+
                    f'settings and customer email is valid and try again. '+
                    f'More info: {str(e)}')
                return redirect(reverse('invoice_list')+f'?filter={filter}')
      
            else:
                # Redirect with success message
                messages.success(request, f'Invoice successfully sent to customer')
                return redirect(reverse('invoice_list')+f'?filter={filter}')                

        invoice.status = new_invoice_status
        invoice.save()        
        messages.success(request, f'Successfully changed invoice status')
        return redirect(reverse('invoice_list')+f'?filter={filter}')

    if request.method == 'GET':
        if 'filter' in request.GET:
            filter = request.GET['filter']

            if 'q' in request.GET:
                query = request.GET['q']
                if not query:
                    messages.error(request, 'Nothing entered in search bar.')
                    return redirect(reverse('invoice_list')) 
                queries = Q(customer__name__icontains=query) | Q(vehicle__registration__icontains=query)
                invoices = invoices.filter(queries)

    status_to_filter = filter_mapping.get(filter)
    if filter == 'inactive':
        invoices=invoices.filter(status__in=status_to_filter).order_by('status')
    else: 
        invoices=invoices.filter(status__in=status_to_filter).order_by('-status')
    # a map for invoice class depending on current status
    status_class_map = {
        1: 'secondary',
        2: 'light',
        3: 'success',
        4: 'info',
        5: 'danger',
        6: 'light'
    } 

    context = {
        'create_invoice_form': create_invoice_form,
        'invoices': invoices,
        'search_term': query,
        'filter_status': filter,
        'status_class_map': status_class_map,
        'available_status_map': available_status_full_dict_map
    }
    return render(request, 'invoice/invoice_list.html', context)


def create_invoice(request):
    form = InvoiceForm(request.POST, request.FILES)
    if form.is_valid():
        invoice = form.save()
        messages.success(request, f'Successfully added invoice')
        return redirect(reverse('invoice_summary', args=[invoice.slug]))
    else:
        messages.error(request, 'Failed to add invoice. Please ensure the form is valid.')
        return redirect(reverse('invoice_list')) 

def edit_invoice(request, slug):
    invoice = get_object_or_404(Invoice, slug=slug)
    form = InvoiceForm(request.POST, request.FILES, instance=invoice)
    if form.is_valid():
        invoice = form.save()
        messages.success(request, f'Successfully edited invoice')
        return redirect(reverse('invoice_summary', args=[invoice.slug]))
    else:
        messages.error(request, 'Failed to edit invoice. Please ensure the form is valid.')
        return redirect(reverse('invoice_summary', args=[invoice.slug])) 

def delete_invoice(request, slug):
    try:
        invoice = get_object_or_404(Invoice, slug=slug)
        invoice.delete()
    except Exception as e:
        messages.error(
            request, f'Failed to delete invoice. More info: {str(e)}')
        return redirect(reverse('invoice_list'))
    else:
        messages.success(request, f'Successfully deleted {invoice}')
        return redirect(reverse('invoice_list'))



def invoice_summary(request, slug):
    """
    A view to return a single-invoice view with product and labour formsets
    """
    # fetch the invoice in question and a create instance of it's form 
    invoice = get_object_or_404(Invoice, slug=slug)
    labour = Labour.objects.filter(invoice=invoice.id)
    parts = Part.objects.filter(invoice=invoice.id)

    if request.method == 'POST':
        invoice_details_form = InvoiceForm(request.POST, request.FILES, instance=invoice)
        part_formset = PartFormSet(request.POST, queryset=parts, instance=invoice, prefix='parts')
        labour_formset = LabourFormSet(request.POST, queryset=labour, instance=invoice, prefix='labour')

        if invoice_details_form.is_valid() and part_formset.is_valid() and labour_formset.is_valid():
            invoice_details = invoice_details_form.save()

            part_instances = part_formset.save(commit=False)
            for form in part_formset:
                # delete any forms with delete checked 
                if form.cleaned_data.get('DELETE'):
                    instance=form.instance
                    instance.delete()
                else:
                    form.save()

            labour_instances = labour_formset.save(commit=False)
            for form in labour_formset:
                if form.cleaned_data.get('DELETE'):
                    instance=form.instance
                    instance.delete()
                else:
                    form.save()
            
            messages.success(request, 'Parts changes saved successfully.')
            return redirect('invoice_summary', slug=slug)
        else:
            messages.error(request, 'Form validation failed. Please check your input.')
            return redirect(reverse('invoice_summary', args=[invoice.slug]))
    else:

        invoice_details_form = InvoiceForm(instance=invoice)
        # fetch list of parts and instantiate formset
        part_formset = PartFormSet(queryset=parts, instance=invoice, prefix='parts')
        part_formset.helper = BasePartFormSetHelper()
        # fetch list of labour entries and instantiate formset
        labour_formset = LabourFormSet(queryset=labour, instance=invoice, prefix='labour')
        labour_formset.helper = BaseLabourFormSetHelper()


        
        # if 'parts-TOTAL_FORMS' in request.POST:
        #     # Handles part formset submission
        #     part_formset = PartFormSet(request.POST, queryset=parts, instance=invoice, prefix='parts')
        #     if part_formset.is_valid():
                # instances = part_formset.save(commit=False)
                # # loop over forms 
                # for form in part_formset:
                #     # delete any forms with delete checked 
                #     if form.cleaned_data.get('DELETE'):
                #         instance=form.instance
                #         instance.delete()
                #     else:
                #         part_formset.save()
        #         messages.success(request, 'Parts changes saved successfully.')
        #         return redirect('invoice_summary', slug=slug)
        #     else:
        #         messages.error(request, 'Parts form validation failed. Please check your input.')
        #         return redirect(reverse('invoice_summary', args=[invoice.slug]))

        # elif 'labour-TOTAL_FORMS' in request.POST:
        #     # Handles labour formset submission
        #     labour_formset = LabourFormSet(request.POST, queryset=labour, instance=invoice, prefix='labour')
        #     if labour_formset.is_valid():
        #         instances = labour_formset.save(commit=False)
        #         for form in labour_formset:
        #             if form.cleaned_data.get('DELETE'):
        #                 instance = form.instance
        #                 instance.delete()
        #             else:
        #                 form.save()
        #         messages.success(request, 'Labour changes saved successfully.')
        #         return redirect('invoice_summary', slug=slug)
        #     else:

        #         messages.error(request, 'Labour form validation failed. Please check your input.')
        #         return redirect(reverse('invoice_summary', args=[invoice.slug]))   

    # a map for invoice class depending on current status
    status_class_map = {
        1: 'light',
        2: 'success',
        3: 'warning',
        4: 'danger',
        5: 'light'
    }   

    context = {
        'item': invoice,
        'previous_url': 'invoice_list',
        'part_formset': part_formset,
        'labour_formset': labour_formset,
        'parts_list': parts,
        'labour_list': labour,
        'edit_invoice_form': invoice_details_form,
        'status_class_map': status_class_map,
        'available_status_map': available_status_full_dict_map
    }
    return render(request, 'invoice/invoice_summary.html', context)
