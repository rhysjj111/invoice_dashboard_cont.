from django.shortcuts import render, redirect, reverse, get_object_or_404
from .forms import InvoiceForm, PartFormSet, BasePartFormSetHelper, LabourFormSet, BaseLabourFormSetHelper
from .models import Invoice, Part, Labour
from django.contrib import messages
from django.db.models import Q


def extract_options(status_options, *keys_to_keep):
    """Extracts keys and values from dictionary"""
    return {key: status_options[key] for key in keys_to_keep}

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
    filter = 'active'

    if request.method == 'POST':
        filter = request.POST.get('filter')
        invoice_pk = request.POST.get('pk')
        invoice_status = int(request.POST.get('status'))
        invoice = get_object_or_404(Invoice, pk=invoice_pk)
        invoice.status = invoice_status
        invoice.save()        
        messages.success(request, f'Successfully')
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
    invoices=invoices.filter(status__in=status_to_filter)

    all_status_options = dict(Invoice.InvoiceStatus.choices)
    # a map for avaiable invoice options depending on current status 
    status_mapping = {
        1: (2,),
        2: (3, 1),
        3: (4, 2),
        4: (5, 3),
        5: (6, 4)
    }

    # a map for invoice class depending on current status
    class_mapping = {
        1: 'table-secondary',
        3: 'table-success',
        4: 'table-warning'
    }

    # append next available invoice status options to invoices
    for invoice in invoices:
        available_status_options = status_mapping.get(invoice.status, {})
        invoice.available_status_options = extract_options(all_status_options, *available_status_options)
        

    context = {
        'create_invoice_form': create_invoice_form,
        'invoices': invoices,
        'search_term': query,
        'filter_status': filter,
        'table_class_dict': class_mapping
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


def invoice_summary(request, slug):
    """
    A view to return a single-invoice view with product and labour formsets
    """
    # fetch the invoice in question and a create instance of it's form 
    invoice = get_object_or_404(Invoice, slug=slug)
    invoice_form = InvoiceForm(instance=invoice)

    # fetch list of parts and instantiate formset
    parts = Part.objects.filter(invoice=invoice.id)
    part_formset = PartFormSet(queryset=parts, instance=invoice, prefix='parts')
    part_formset.helper = BasePartFormSetHelper()

    # fetch list of labour entries and instantiate formset
    labour = Labour.objects.filter(invoice=invoice.id)
    labour_formset = LabourFormSet(queryset=labour, instance=invoice, prefix='labour')
    labour_formset.helper = BaseLabourFormSetHelper()


    if request.method == 'POST':
        if 'parts-TOTAL_FORMS' in request.POST:
            # handles part formset submission
            part_formset = PartFormSet(request.POST, queryset=parts, instance=invoice, prefix='parts')
            if part_formset.is_valid():
                instances = part_formset.save(commit=False)
                # loop over forms 
                for form in part_formset:
                    # delete any forms with delete checked 
                    if form.cleaned_data.get('DELETE'):
                        instance=form.instance
                        instance.delete()
                    else:
                        part_formset.save()
                messages.success(request, 'Parts changes saved successfully.')
                return redirect('invoice_summary', slug=slug)
            else:
                messages.error(request, 'Parts form validation failed. Please check your input.')
                return redirect(reverse('invoice_summary', args=[invoice.slug]))

        elif 'labour-TOTAL_FORMS' in request.POST:
            # handles labour formset submission
            labour = Labour.objects.filter(invoice=invoice.id)
            labour_formset = LabourFormSet(request.POST, queryset=labour, instance=invoice, prefix='labour')
            if labour_formset.is_valid():
                instances = labour_formset.save(commit=False)
                for form in labour_formset:
                    if form.cleaned_data.get('DELETE'):
                        instance = form.instance
                        instance.delete()
                    else:
                        form.save()
                        print(form.cleaned_data['hours'])
                messages.success(request, 'Labour changes saved successfully.')
                return redirect('invoice_summary', slug=slug)
            else:

                messages.error(request, 'Labour form validation failed. Please check your input.')
                return redirect(reverse('invoice_summary', args=[invoice.slug]))
    else:
        part_formset = PartFormSet(queryset=parts, instance=invoice, prefix='parts')
        part_formset.helper = BasePartFormSetHelper()
        labour_formset = LabourFormSet(queryset=labour, instance=invoice, prefix='labour')
        labour_formset.helper = BaseLabourFormSetHelper()       

    context = {
        'item': invoice,
        'previous_url': 'invoice_list',
        'part_formset': part_formset,
        'labour_formset': labour_formset,
        'parts_list': parts,
        'labour_list': labour,
        'edit_invoice_form': invoice_form,
    }
    return render(request, 'invoice/invoice_summary.html', context)
