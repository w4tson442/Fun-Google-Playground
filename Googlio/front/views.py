from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from .models import Email

# =========================================================================

#main page
def index(request):
    template = loader.get_template('front/index.html')
    context = {
        'place_holder': 'Enter Your Email',
    }
    return HttpResponse(template.render(context, request))

#main dashbard
def dashboard(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

#GET REQUEST
def send(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

# =========================================================================

#HP(helper)
#saves a gmail to the database
#1. check to see if the username exists
#2. if it does update instead of creating an new one
def saveGmail():
    return "test test"  
