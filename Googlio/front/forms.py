from django import forms

#Examples of form fields:
#    subject = forms.CharField(max_length=100)
#    message = forms.CharField(widget=forms.Textarea)
#    sender = forms.EmailField()
#    cc_myself = forms.BooleanField(required=False)
# link: https://docs.djangoproject.com/en/3.1/topics/forms/

class GmailForm(forms.Form):
    email = forms.EmailField(label='Your Email')
