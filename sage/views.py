from django.shortcuts import render, redirect, reverse, get_object_or_404
import requests
import os
from requests_oauthlib import OAuth2Session

# Sage Accounting API endpoints
AUTH_URL = 'https://www.sageone.com/oauth2/auth/central?filter=apiv3.1'
TOKEN_URL = 'https://oauth.accounting.sage.com/token'

# Your Sage Accounting app credentials
CLIENT_ID = os.environ.get('CLIENT_ID', '')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET', '')
REDIRECT_URI = os.environ.get('REDIRECT_URI')  # The URL Sage Accounting will redirect back to after authorization

def test(request):
    """A view to return the landing page for customer payment"""

    template = 'sage/test.html'

    context = {
    }

    return render(request, template, context)


def sage_auth(request):
    sage = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)
    authorization_url, state = sage.authorization_url(AUTH_URL)
    print(authorization_url)

    # Store the state in the session for later verification
    request.session['oauth_state'] = state

    return redirect(authorization_url)

def sage_callback(request):
    # Ensure the state returned in the callback matches the one we stored
    if request.GET.get('state') != request.session.get('oauth_state'):
        return HttpResponseBadRequest("Invalid OAuth state")

    sage = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)
    token = sage.fetch_token(TOKEN_URL, client_secret=CLIENT_SECRET, authorization_response=request.build_absolute_uri())

    # Store the access token in the session or database for future use
    request.session['sage_access_token'] = token

    return HttpResponse("Authentication successful. You can now make API requests.")

# Make API requests using the access token
def make_api_request(request):
    access_token = request.session.get('sage_access_token')
    if not access_token:
        return HttpResponseBadRequest("No access token found. Please authenticate first.")

    sage = OAuth2Session(CLIENT_ID, token=access_token)
    response = sage.get('SAGE_ACCOUNTING_API_ENDPOINT')

    # Handle the API response as needed
    return HttpResponse(response.json())