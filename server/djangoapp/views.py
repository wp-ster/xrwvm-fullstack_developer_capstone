from .restapis import get_request, analyze_review_sentiments, post_review
import json

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from datetime import datetime
import logging
from django.views.decorators.csrf import csrf_exempt

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

def get_dealerships(request, state="All"):
    if(state == "All"):
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/" + state
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = "/fetchDealer/" + str(dealer_id)
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = "/fetchReviews/dealer/" + str(dealer_id)
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail.get('review', ''))
            review_detail['sentiment'] = response.get('sentiment', 'neutral') if response else 'neutral'
        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


def get_cars(request):
    """Return list of cars for review form dropdown"""
    cars_list = [
        {"make": "Toyota", "model": "Camry"},
        {"make": "Toyota", "model": "Corolla"},
        {"make": "Honda", "model": "Civic"},
        {"make": "Honda", "model": "Accord"},
        {"make": "Ford", "model": "Focus"},
        {"make": "Ford", "model": "Mustang"},
        {"make": "BMW", "model": "3 Series"},
        {"make": "BMW", "model": "5 Series"},
        {"make": "Mercedes", "model": "C-Class"},
        {"make": "Mercedes", "model": "E-Class"},
        {"make": "Audi", "model": "A4"},
        {"make": "Audi", "model": "A6"},
        {"make": "Nissan", "model": "Altima"},
        {"make": "Nissan", "model": "Sentra"},
        {"make": "Hyundai", "model": "Elantra"},
        {"make": "Hyundai", "model": "Sonata"},
        {"make": "Chevrolet", "model": "Malibu"},
        {"make": "Chevrolet", "model": "Cruze"}
    ]
    return JsonResponse({"status": 200, "cars": cars_list})


@csrf_exempt
def add_review(request):
    if not request.user.is_anonymous:
        try:
            data = json.loads(request.body)
            response = post_review(data)
            return JsonResponse({"status": 200})
        except Exception as e:
            logger.error(f"Error in posting review: {e}")
            return JsonResponse({"status": 401, "message": "Error in posting review"})
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized"})


@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data.get('userName', '')
    password = data.get('password', '')

    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)


@csrf_exempt
def logout_request(request):
    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)


@csrf_exempt
def registration(request):
    data = json.loads(request.body)
    username = data.get('userName', '')
    password = data.get('password', '')
    first_name = data.get('firstName', '')
    last_name = data.get('lastName', '')
    email = data.get('email', '')
    username_exist = False

    try:
        User.objects.get(username=username)
        username_exist = True
    except User.DoesNotExist:
        logger.debug(f"{username} is new user")

    if not username_exist:
        user = User.objects.create_user(username=username, first_name=first_name,
                                      last_name=last_name, password=password, email=email)
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})
    else:
        return JsonResponse({"userName": username, "error": "Already Registered"})


