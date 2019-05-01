from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail

# Create your views here.
from contacts.models import Contact


def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        if request.user.is_authenticated:
            # user_id = request.POST['user_id']
            has_contacted = Contact.objects.all().filter(user_id=user_id,listing_id=listing_id)
            if has_contacted:
                messages.error(request,"You have already made an inquiry for this home")
                return redirect('/listings/'+listing_id)

        contact = Contact(listing=listing, listing_id=listing_id, name=name, email=email, phone=phone,
                          message=message, user_id=user_id)
        contact.save()

        # send email
        send_mail(
            'Property Listing Inquiry',
            'there has been inquiry for this house'+listing + '.Sign in to admin panel for more info',
            'vijaydhakal48@gmail.com',
            [realtor_email,'vijaydhakal49@gmail.com'],
            fail_silently=False
        )

        messages.success(request, "Your inquiry has been made successfully, Realtor will get to you soon")
        return redirect('/listings/' + listing_id)
