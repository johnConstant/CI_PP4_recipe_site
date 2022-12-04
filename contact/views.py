from django.shortcuts import render, redirect
from django.views import generic, View
from django.contrib import messages

from .forms import ContactForm


class Contact(View):
    """
    A class view for the contact page
    """
    def get(self, request, *args, **kwargs):
        form = ContactForm({
            'name': request.user.username,
            })
        context = {
            'contact_form': form
        }
        return render(request, 'contact.html', context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent.")
            return redirect('/')
