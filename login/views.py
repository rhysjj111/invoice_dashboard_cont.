from django.shortcuts import render


def index(request):
    """A view to return login page"""
    context = {
    }
    return render(request, 'login/index.html', context)