# sendemail/views.py
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import ContactForm
from django.conf import settings

def privacy(request):
   return render(request, "privacy.html", {})

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            email_subject = f'New contact {form.cleaned_data["from_email"]}: {form.cleaned_data["subject"]}'
            email_message = form.cleaned_data['message']
            request.session['from_email'] = form.cleaned_data["from_email"]
            send_mail(email_subject, email_message, settings.CONTACT_EMAIL, settings.ADMIN_EMAIL)
            return render(request, 'emailsuccess.html')
    form = ContactForm()
    context = {'form': form}
    return render(request, 'email.html', context)

def contactView(request):
    if request.method == "GET":
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = f'New contact {form.cleaned_data["from_email"]}: {form.cleaned_data["subject"]}'
            from_email = form.cleaned_data["from_email"]
            message = form.cleaned_data['message']
            request.session['from_email'] = from_email
            try:
                send_mail(subject, message, settings.CONTACT_EMAIL, settings.ADMIN_EMAIL)
            except BadHeaderError:
                return HttpResponse("Invalid header found.")
            return redirect("success")
    return render(request, "email.html", {"form": form})

def successView(request):
    from_email = request.session.get('from_email')
    return render(
            request=request,
            template_name="emailsuccess.html",
            context={"from_email": from_email}
            )