from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import DealerReview, CarDealer, CarModel
from .restapis import get_dealers_from_cf, post_request, get_dealership_reviews_from_db,\
    get_dealer_from_cf, post_dealership_review_to_db, get_dealer_by_state_from_cf
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
    View for dealership details using id.
    """
    if request.method == "GET":
        dealership = get_dealer_from_cf(dealer_id)
        context = {
            'dealership_details': dealership,
        }

        return render(request, 'base/dealership.html', context)


def get_dealership_by_st(request, dealer_st):
    """
    View for dealership details using st.
    """
    if request.method == "GET":
        dealership = get_dealer_by_state_from_cf(dealer_st)

        return HttpResponse(dealership)


def get_dealership_reviews(request, dealer_id):
    """
    View for dealership reviews.
    Renders a list of all reviews for a dealership.
    """
    if request.method == "GET":
        reviews = get_dealership_reviews_from_db(dealer_id)
        dealership_query = get_dealer_from_cf(dealer_id)
        dealership_details = {}
        for dealership in dealership_query:
            dealership_details["full_name"] = dealership.full_name
            dealership_details["id"] = dealership.id

        context = {
            'reviews': reviews,
            'dealership_details': dealership_details,
        }

        return render(request, 'base/dealer_details.html', context)


def add_review(request, dealer_id):
    """
    View for creating a new review.
    """
    if request.method == "GET":
        cars = CarModel.objects.filter(dealerId=dealer_id)
        dealership_details = {}
        dealership_query = get_dealer_from_cf(dealer_id)
        for dealership in dealership_query:
            dealership_details["full_name"] = dealership.full_name
            dealership_details["id"] = dealership.id

        context = {
            'cars': cars,
            'dealership_details': dealership_details
        }

        return render(request, 'base/add_review.html', context)

    # if request.user.is_authenticated:
    if request.method == "POST" and request.user.is_authenticated:
        user_id = request.user.id
        review = {}
        json_payload = {}

        review["dealership"] = int(request.POST['dealership_id'])
        review["name"] = request.POST['user_full_name']
        review["review"] = request.POST['content']
        purchase_check = request.POST['purchasecheck']
        if purchase_check == 'on':
            purchase = True
        else:
            purchase = False
        review["purchase"] = purchase
        review["purchase_date"] = request.POST['purchasedate']
        car_id = request.POST['car']
        car = CarModel.objects.get(id=car_id)
        review["car_make"] = car.make.name
        review["car_model"] = car.name
        review["car_year"] = car.year.strftime("%Y")
        review["sentiment"] = " "

        json_payload["review"] = review

        result = post_dealership_review_to_db(json_payload)
        print(result)

        return redirect('base:dealer_details', dealer_id=dealer_id)
