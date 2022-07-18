from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.forms import ModelForm, Textarea
from .models import DealerReview, CarDealer, CarModel
from .restapis import get_dealers_from_cf, post_request, get_dealership_reviews_from_db, get_dealer_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


def about(request):
    """
    View for the About page.
    """
    context = {
    }
    if request.method == "GET":
        return render(request, 'base/about.html', context)


def contact(request):
    """
    View for the Contact page.
    """
    context = {
    }
    if request.method == "GET":
        return render(request, 'base/contact.html', context)


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
            # Directs user to home page if login is successful.
            return redirect('base:index')
        else:
            messages.error(request, 'Username/Password do not match')
            return redirect('base:login')

    else:
        return render(request, 'base/login.html')


def logout_request(request):
    """
    View for logging out.
    """
    logout(request)
    messages.success(request, 'Logged out')
    # Directs user to home page if logout is successful.
    return redirect('base:index')


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


def get_dealerships(request):
    """
    View for the Home page/index.
    Renders a list of all dealerships.
    """
    context = {}
    if request.method == "GET":
        url = "https://8f6ed1e1.us-south.apigw.appdomain.cloud/api/dealership"
        dealerships = get_dealers_from_cf(url)
        context = {'dealership_list': dealerships}
        return render(request, 'base/index.html', context)


def get_dealership_by_id(request, dealer_id):
    """

    """
    if request.method == "GET":
        dealership = get_dealer_from_cf(dealer_id)
        context = {'dealership_details': dealership}

        # return HttpResponse(dealership)
        return render(request, 'base/dealership.html', context)


def get_dealership_reviews(request, dealer_id):
    if request.method == "GET":
        reviews = get_dealership_reviews_from_db(dealer_id)
        dealership_details = get_dealer_from_cf(dealer_id)

        context = {
            'reviews': reviews,
            'dealership_details': dealership_details
        }
        # return HttpResponse(reviews)
        return render(request, 'base/dealer_details.html', context)


# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    # check is user is authenticated
    if request.user.is_authenticated:
        user_id = request.user.id
        url = "https://8f6ed1e1.us-south.apigw.appdomain.cloud/api/review"

        review = {}
        json_payload = {'review': review}
        results = post_request(url, json_payload, dealer_id=dealer_id)
        print(results)
        return HttpResponse(results)



# def add_review(request, dealer_id):
#     dealer = get_object_or_404(CarDealer, pk=dealer_id)
#     if request.method == "GET":
#         cars = CarModel.objects.get(DealerId=dealer_id)
#         context = {'cars': cars}
#         return render(request, 'base/add_review.html', context)
#     else:
#         if request.user.is_authenticated:
#             user_id = request.user.id
#         form = ReviewForm(request.POST)
#         if form.is_valid():
#             name = form.cleaned_data['name']
#             dealership = form.cleaned_data['dealership']
#             review = form.cleaned_data['review']
#             purchase = form.cleaned_data['purchase']
#             purchase_date = form.cleaned_data['purchase_date']
#             car_make = form.cleaned_data['car_make']
#             car_model = form.cleaned_data['car_model']
#             car_year = form.cleaned_data['car_year']
#
#             review_doc = DealerReview()
#             review_doc.name = name,
#             review_doc.dealership = dealership
#             review_doc.review = review
#             review_doc.purchase = purchase
#             review_doc.purchase_date = purchase_date
#             review_doc.car_make = car_make
#             review_doc.car_model = car_model
#             review_doc.car_year = car_year
#             review_doc.save()
#
#             return redirect("base:dealer_details", dealer_id=dealer_id)
