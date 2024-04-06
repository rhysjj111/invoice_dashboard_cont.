def user_creds(request):
    return {
        'Mechanic': request.user.groups.filter(name='Mechanic').exists(),
        'Accounts': request.user.groups.filter(name='Accounts').exists(),
        'Foreman': request.user.groups.filter(name='Foreman').exists(),
        'test': request.user.groups.first(),
    }

