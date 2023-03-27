from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    """
    A class view creating the Contact form
    """
    class Meta:
        model = Contact
        fields = ['name', 'email', 'category', 'message', 'email_subscription']
