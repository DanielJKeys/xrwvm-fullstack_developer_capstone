from django.shortcuts import render 
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from datetime import datetime
from .restapis import get_request, analyze_review_sentiments, post_review

from django.http import JsonResponse
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate
# Import your models (Ensure these are defined in your models.py)
# from .models import CarMake, CarModel 

# Get an instance of a logger
logger = logging.getLogger(__name__)

@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)

# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exist = False
    
    try:
        # Check if user already exists
        User.objects.get(username=username)
        username_exist = True
    except:
        # If not, simply log that this is a new user
        logger.debug("{} is new user".format(username))

    # If it is a new user
    if not username_exist:
        # Create user in auth_user table
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password, email=email)
        # Login the user and return success
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})
    else:
        return JsonResponse({"userName": username, "error": "Already Registered"})

# Update the `get_dealerships` view to render the index page with a list of dealerships
# Note: This usually interfaces with a backend service or your local DB
def get_dealerships(request, state="All"):
    if state == "All":
        # Placeholder for actual database call or external API call
        # dealerships = get_dealers_from_cf() 
        return HttpResponse("List of all dealerships") # Replace with render() or JsonResponse()
    else:
        # dealerships = get_dealers_by_state_from_cf(state)
        return HttpResponse(f"List of dealerships in {state}")

# Create a `get_dealer_reviews` view to render the reviews of a dealer
def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        # reviews = get_dealer_reviews_from_cf(dealer_id)
        return JsonResponse({"status": 200, "reviews": []}) # Replace with actual data
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

# Create a `get_dealer_details` view to render the dealer details
def get_dealer_details(request, dealer_id):
    if dealer_id:
        # dealer = get_dealer_by_id_from_cf(dealer_id)
        return JsonResponse({"status": 200, "dealer": {}}) # Replace with actual data
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

# Create a `add_review` view to submit a review
@csrf_exempt
def add_review(request):
    if not request.user.is_anonymous:
        data = json.loads(request.body)
        try:
            # post_review(data) # Logic to post to your sentiment analyzer/cloudant
            return JsonResponse({"status": 200})
        except:
            return JsonResponse({"status": 401, "message": "Error in posting review"})
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized"})