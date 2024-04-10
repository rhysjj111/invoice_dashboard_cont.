import os
from django.conf import settings

def get_domain(request):
    if 'DYNO' in os.environ:  # Running on Heroku
        return 'https://' + settings.ALLOWED_HOSTS[0]
    else:  # Running locally
        return 'https://' + settings.ALLOWED_HOSTS[1]

def user_group_contains(request, group_name):
    return request.user.groups.filter(name=group_name).exists()