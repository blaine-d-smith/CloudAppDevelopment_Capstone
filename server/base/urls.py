from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'base'
urlpatterns = [
    path(
        'about',
        views.about,
        name='about'
    ),
    path(
        'contact',
        views.contact,
        name='contact'
    ),
    path(
        'registration/',
        views.registration_request,
        name='registration'
    ),
    path(
        'login/',
        views.login_request,
        name='login'
    ),
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
    path(
        'dealer/<int:dealer_id>/',
        views.get_dealership_reviews,
        name='dealer_details'
    ),
    path(
        'dealership/<int:dealer_id>/',
        views.get_dealership_by_id,
        name='dealership'
    ),
    path(
        'add_review/<int:dealer_id>/',
        views.add_review,
        name='add_review'
    ),
]
