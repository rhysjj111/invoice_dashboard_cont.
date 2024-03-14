from django.shortcuts import render

def customer_list(request):
    """A view to return main customer view"""
    previous_url = 'customer_list'
    delete_url = 'customer_list'
    context = {
        'previous_url': 'customer_list',
        'delete_url': delete_url,
    }
    return render(request, 'customer/customer_list.html', context)


def customer_summary(request):
    """A view to return a single-customer view"""
    previous_url = 'customer_list'
    delete_url = 'customer_list'
    context = {
        'previous_url': 'customer_list',
        'delete_url': delete_url,
    }
    return render(request, 'customer/customer_summary.html', context)
