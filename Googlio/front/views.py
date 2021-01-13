import os
from pathlib import Path
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from .models import Email
from .forms import GmailForm
import google.oauth2.credentials
import google_auth_oauthlib.flow

# =========================================================================

#                    --------------------------------------------
# HELP: How to Get object from Database (https://docs.djangoproject.com/en/3.1/intro/tutorial03/)
# try:
#     question = Question.objects.get(pk=question_id)
# except Question.DoesNotExist:
#     raise Http404("Question does not exist")
# <OR>
# question = get_object_or_404(Question, pk=question_id)
#                    --------------------------------------------

#main page
def index(request):
    template = loader.get_template('front/index.html')
    form = GmailForm()
    context = {
        'place_holder': 'Enter Your Email',
        'form' : form,
    }
    return HttpResponse(template.render(context, request))

#main dashbard
def dashboard(request, question_id):
    context = {
        'User' : '0'
    }
    return render(request, 'front/index.html', context)

#GET REQUEST
def send(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = GmailForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            email = form.cleaned_data['email']
            auth_url = askGoogle(str(email));
            return redirect(auth_url);

    # if a GET (or any other method) we'll create a blank form
    else:
        form = GmailForm()
    return HttpResponse("hello")

#GET Concent Screen Url
# return: authorization_url
# check: state
#reference link: https://developers.google.com/identity/protocols/oauth2/web-server#python_1
def askGoogle(email):
    CLIENT_SECRET = os.path.join(os.path.dirname(__file__), 'client_secret.json')
    SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        str(CLIENT_SECRET),
        SCOPES,
    )

    flow.redirect_uri = 'http://127.0.0.1:8080/front/tyGoogle'

    authorization_url, state = flow.authorization_url(
        access_type='offline', prompt='consent', login_hint=email,
    include_granted_scopes='true')

    return authorization_url

#Return Url function
def tyGoogle(response):
    auth_code = ''
    if response.method == 'GET':
        query_body = response.GET
        if 'code' in query_body:
            auth_code = query_body.get('code')

    print_this = str(query_body) + ' | ' + str(auth_code)
    printFile('test_test.txt', print_this)
    return redirect('google.com')

#DeBug Purpose 
def printFile(file_name, contents):
    TEST_OUTPUT = os.path.join(os.path.dirname(__file__), file_name)
    f = open(TEST_OUTPUT, "w")
    f.write(contents)
    f.close()

# =========================================================================

#HP(helper)
#saves a gmail to the database
#1. check to see if the username exists
#2. if it does update instead of creating an new one
def saveGmail():
    return "test test"  
