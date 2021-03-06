import os
import json
import datetime
import calendar
from tzlocal import get_localzone
from pathlib import Path
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.conf import settings
from .models import Email
from .models import Event
from .forms import GmailForm
from .utils import Calendar
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
    try:
        credentials = getCred(request.session.get('email'))
    except:
        return redirect('/front/')

    getEvents(credentials)
    try: #sometimes the scope changes and everything changes which sucks 
        formatted_files = getDriveFiles(credentials)
        formatted_gmails = getUserEmail(credentials)
        calendar = getCalendar(request.GET.get('day', None))
    except:
        auth_url = askGoogle(request, request.session.get('email'))
        return redirect(auth_url)
    context = {
        'formatted_files'  : formatted_files,
        'formatted_gmails' : formatted_gmails,
        'calendar'         : mark_safe(calendar),
    }
    return render(request, 'front/dashboard.html', context)

#reference: https://developers.google.com/calendar/v3/reference/events/list#examples
def getEvents(credentials):
    service = build('calendar', 'v3', credentials=credentials)
    calendarList = service.calendarList().list().execute()

    #get first calendar
    cal_choice = {}
    cal_choice[calendarList['items'][0]['id']] = calendarList['items'][0]['summary']

    #get year and month
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    #generate dates for first day and last day
    fday = str(year) + "-" + str(month) +   "-1"
    lday = str(year) + "-" + str(month+1) + "-1"

    timeMin = datetime.datetime.strptime(fday, "%Y-%m-%d").astimezone(get_localzone()).isoformat()
    timeMax = datetime.datetime.strptime(lday, "%Y-%m-%d").astimezone(get_localzone()).isoformat()

    eventList = service.events().list(
            calendarId='primary',
            timeMin=timeMin,
            timeMax=timeMax,
    ).execute()

    for event in eventList['items']:
        #check if event exists with google_id
        try:
            event_model = Event.objects.get(google_id=event['id'])
        except:
            event_model = Event(google_id=event['id'])

        #if etag doesn't exist or is outdated
        # !Tried to save dates as isoformat but it is hard
        printFile('test.txt', json.dumps(event))
        if event_model.google_etag != event['etag']:
            if 'description' in event:
                event_model.description = event['description']

            if 'colorId' in event:
                event_model.colorId = getEventColor(event['colorId'])
            else:
                event_model.colorId = getEventColor(0)

            if 'dateTime' in event['start']:
                event_model.start_time  = event['start']['dateTime']
                event_model.end_time    = event['end']['dateTime']
            else:
                event_model.start_time  = event['start']['date']
                event_model.end_time    = event['end']['date']

            event_model.google_etag = event['etag']
            event_model.title       = event['summary']
            event_model.save()

#reference: https://www.huiwenteo.com/normal/2018/07/24/django-calendar.html
def getCalendar(date):
    # use today's date for the calendar
    d = get_date(date)

    # Instantiate our calendar class with today's year and date
    cal = Calendar(d.year, d.month)

    # Call the formatmonth method, which returns our calendar as a table
    html_cal = cal.formatmonth(withyear=True)

    calendar = html_cal
    return calendar

#reference:https://developers.google.com/gmail/api/reference/rest/v1/users.messages/list
#reference:https://support.google.com/mail/answer/7190
def getUserEmail(credentials):
    gmail = build('gmail', 'v1', credentials=credentials)
    emails = gmail.users().messages().list(
            maxResults=30,
            userId='me',
            q='is:unread AND NOT label:promotions AND NOT label:social',
            includeSpamTrash=False,
    ).execute()
    formatted_gmails = []
    for email  in emails['messages']:
        new_email = gmail.users().messages().get(
                userId='me',
                id=email['id'],
        ).execute()
        new_email = getInfo(new_email)
        formatted_gmails.append(new_email)
    return formatted_gmails

#reference: https://developers.google.com/drive/api/v2/reference/files
def getDriveFiles(credentials):
    drive = build('drive', 'v2', credentials=credentials)
    files = drive.files().list().execute()
    formatted_files = []
    if 'items' in files:
        for doc in files['items']:
           if 'lastModifyingUser' in doc:
               emailAddress = doc['lastModifyingUser']['emailAddress']
               displayName = doc['lastModifyingUser']['displayName']
           else:
               emailAddress = 'no email'
               displayName = 'unavailable'
           newItem = {
                   'id' : doc['id'],
                   'title' : doc['title'],
                   'shared' : doc['shared'],
                   'iconLink' : doc['iconLink'],
                   'viewed' : doc['labels']['viewed'],
                   'embedLink' : doc['embedLink'],
                   'lm_emailAddress' : emailAddress,
                   'lm_displayName' : displayName,
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

#get information of each unread emails
#https://developers.google.com/gmail/api/reference/rest/v1/users.messages/get
def getInfo(new_email):
    list_attr = ['Subject', 'From', 'To']
    result = {}
    result['internalDate'] = formatDate(int(new_email['internalDate']), 2)
    headers = new_email['payload']['headers']
    for header in headers:
        if header['name'] in list_attr:
            result[header['name']] = header['value']
    return result

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.datetime.today()

#reference: https://www.delftstack.com/howto/python/python-convert-epoch-to-datetime/
def formatDate(date, case=1):
    if case == 1:
        newDate = datetime.datetime.strptime(date,"%Y-%m-%dT%H:%M:%S.%fZ").date()
    elif case == 2:
        newDate = datetime.datetime.fromtimestamp(date/1000).strftime('%A, %B %-d, %Y %I:%M %p')
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

#reference: https://lukeboyle.com/blog-posts/2016/04/google-calendar-api---color-id
def getEventColor(colorId = 0):
    ref = {
        0  : '#039be5',
        1  : '#7986cb',
        2  : '#33b679',
        3  : '#8e24aa',
        4  : '#e67c73',
        5  : '#f6c026',
        6  : '#f5511d',
        7  : '#039be5',
        8  : '#616161',
        9  : '#3f51b5',
        10 : '#0b8043',
        11 : '#d60000',
    }
    if int(colorId) >= 0 and int(colorId) <= 11:
        return ref[int(colorId)]
    else:
        return ref[0]
