from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create an `about` view to render a static about page
def about(request):
    """
    View for the About page.
    """
    context = {

    }
    if request.method == "GET":
        return render(request, 'base/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    """
    View for the Contact page.
    """
    context = {

    }
    if request.method == "GET":
        return render(request, 'base/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    """
    Displays a login form for accounts.
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Welcome')
            # Directs user to dashboard if login is successful.
            return redirect('base:index')
        else:
            messages.error(request, 'Username/Password do not match')
            return redirect('base:login')

    else:
        return render(request, 'base/login.html')

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    """
    View for logging out.
    """
    logout(request)
    messages.success(request, 'Logged out')
    # Directs user to home page if logout is successful.
    return redirect('base:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    """
    Displays a form for new account registration.
    Validates username and password.
    Creates a new account with the information from the registration form.
    """
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['psw']
        password2 = request.POST['psw2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect('base:registration')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already exists')
                    return redirect('base:registration')
                else:
                    user = User.objects.create_user(
                        username=username,
                        password=password,
                        email=email,
                        first_name=first_name,
                        last_name=last_name,
                    )

                    user.save()
                    # Redirects to login page
                    return redirect('base:login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('base:registration')

    else:
        return render(request, 'base/registration.html')

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    """
    View for the Home page/index.
    """
    context = {
    }
    if request.method == "GET":
        return render(request, 'base/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

