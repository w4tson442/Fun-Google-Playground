from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from .models import Email
from .forms import GmailForm

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
            return HttpResponse('Thanks! ' + str(email))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = GmailForm()
    return HttpResponse("hello")

# =========================================================================

#HP(helper)
#saves a gmail to the database
#1. check to see if the username exists
#2. if it does update instead of creating an new one
def saveGmail():
    return "test test"  
