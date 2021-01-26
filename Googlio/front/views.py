import os
import json
from pathlib import Path
from datetime import datetime
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.conf import settings
from .models import Email
from .forms import GmailForm
from googleapiclient.discovery import build
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
            if Email.objects.filter(gmail=email).exists():
                email_model = Email.objects.get(gmail=email)
                return redirect('/front/dashboard/')
            else:
                auth_url = askGoogle(request, str(email))
                return redirect(auth_url)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = GmailForm()
    return HttpResponse("hello")

#GET Concent Screen Url
# return: authorization_url
# check: state
#reference link: https://developers.google.com/identity/protocols/oauth2/web-server#python_1
def askGoogle(request, email):
    request.session['email'] = email
    try:
        email_model = Email.objects.get(gmail=email)
    except:
        email_model = Email(gmail=email)
        email_model.save()

    flow = getFlow()

    authorization_url, state = flow.authorization_url(
        access_type='offline', prompt='consent', login_hint=email,
    include_granted_scopes='true')

    return authorization_url

#Return Url function
def tyGoogle(request):
    if request.method == 'GET':
        query_body = request.GET
        if 'code' in query_body:
            access_token = ''
            flow = getFlow()
            flow.fetch_token(code=query_body.get('code'))
            credentials = flow.credentials
            saveCred(request.session.get('email'), credentials)

    return redirect('/front/dashboard/')

#Use code recieved from tyGoogle to get all context
def dashboard(request):
    credentials = getCred(request.session.get('email'))
    try: #sometimes the scope changes and everything changes which sucks 
        formatted_files = getDriveFiles(credentials)
    except:
        auth_url = askGoogle(request, request.session.get('email'))
        return redirect(auth_url)
    context = {
        'formatted_files' : formatted_files
    }
    return render(request, 'front/dashboard.html', context)

def getDriveFiles(credentials):
    drive = build('drive', 'v2', credentials=credentials)
    files = drive.files().list().execute()
    formatted_files = []
    if 'items' in files:
        for doc in files['items']:
           newItem = {
                   'id' : doc['id'],
                   'title' : doc['title'],
                   'embedLink' : doc['embedLink'],
                   'createdDate' : formatDate(doc['createdDate']),
                   'modifiedDate' : formatDate(doc['modifiedDate']),
           }
           formatted_files.append(newItem)
    return formatted_files

# =========================================================================
#HP(helper)
#help Links:
# 1. https://developers.google.com/identity/protocols/oauth2/web-server#python_1

#convert str -> dict -> google.credential object
def getCred(email):
    email_model = Email.objects.get(gmail=email)
    cred = google.oauth2.credentials.Credentials(
          email_model.token,
          refresh_token = email_model.refresh_token,
          token_uri = email_model.token_uri,
          client_id = settings.CLIENT_ID,
          client_secret = email_model.client_secret,
          scopes = settings.SCOPES,
    )
    return cred

def saveCred(email, credentials):
    email_model = Email.objects.get(gmail=email)
    email_model.token = credentials.token
    email_model.refresh_token = credentials.refresh_token
    email_model.token_uri = credentials.token_uri
    email_model.client_secret = credentials.client_secret
    email_model.save()

def formatDate(date):
    newDate = datetime.strptime(date,"%Y-%m-%dT%H:%M:%S.%fZ").date()
    return str(newDate)

#DeBug Purpose
def printFile(file_name, contents):
    TEST_OUTPUT = os.path.join(os.path.dirname(__file__), file_name)
    f = open(TEST_OUTPUT, "w")
    f.write(contents)
    f.close()

def getFlow():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        str(settings.CLIENT_SECRET),
        settings.SCOPES,
    )
    flow.redirect_uri = settings.REDIRECT_URI
    return flow
