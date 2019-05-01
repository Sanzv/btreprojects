from django.shortcuts import render, redirect
from django.contrib import messages ,auth
from django.contrib.auth.models import User


# Create your views here.
from contacts.models import Contact


def register(request):
    if request.method == 'POST':

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # check if password match
        if password == password2:

            # check if username exists

            if User.objects.filter(username=username).exists():
                messages.error(request, "That username is taken")
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, "The email is already registered")
                    return redirect('register')
                else:

                    #         looks good
                    # register user
                    user = User.objects.create_user(username=username, password =password, first_name = first_name,
                                                    last_name=last_name, email=email)
                    user.save()
                    messages.success(request, 'You are now registered and can now login')
                    return redirect('login')
        #         if direct login after register
        #             auth.login(request, user) and you can redirect where necessary

        else:
            messages.error(request, "Password does not match")
            return redirect('register')
        # messages.error(request, "Testing error message")
        # return redirect('register')

    else:
        return render(request, 'accounts/register.html')


def login(request):
    if request.method == 'POST':
        # login user
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are now logged in")
            return redirect('dashboard')
        else:
            messages.error(request, "Either username or password is wrong")
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, "You are now logout")

    return redirect('index')


def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)
    context ={
        'contacts': user_contacts
    }
    return render(request, 'accounts/dashboard.html', context)
