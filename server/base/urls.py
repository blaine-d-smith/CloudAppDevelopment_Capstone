from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'base'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    # path for about view
    path(
        'about',
        views.about,
        name='about'
    ),
    # path for contact us view
    path(
        'contact',
        views.contact,
        name='contact'
    ),

    # path for registration
    path(
        'registration/',
        views.registration_request,
        name='registration'
    ),
    # path for login
    path(
        'login/',
        views.login_request,
        name='login'
    ),

    # path for logout
    path(
        'logout/',
        views.logout_request,
        name='logout'
    ),
    path(
        '',
        views.get_dealerships,
        name='index'
    ),
    # path for dealer reviews view
    path(
        'dealer/<int:dealer_id>/',
        # views.get_dealer_details,
        views.get_dealership_reviews,
        name='dealer_details'
        # name='dealership_reviews'
    ),
    path(
        'dealership/<int:dealer_id>/',
        views.get_dealership_by_id,
        name='dealership'
    ),
    # path for add a review view
    path(
        'add_review/<int:dealer_id>/',
        views.add_review,
        name='add_review'
    ),
]
