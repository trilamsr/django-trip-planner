from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.
def reroute(request):
    return redirect('/')

def main (request):
    if 'user_id' not in request.session:
        return render(request, 'main/login_reg.html')
    else:
        logged_user = User.objects.get(id=request.session['user_id'])
        return render(request, 'main/dashboard.html', {'user': logged_user, 'alltrips':Trip.objects.all()})

def register(request):
    if request.method =='GET':
        return redirect('/')
    else:
        error = {}
        User.objects.validate_reg_name(error, request.POST)
        User.objects.validate_birthday(error, request.POST)
        User.objects.validate_reg_email(error, request.POST)
        User.objects.validate_registration_password(error, request.POST)
        if len(error) > 0:
            for k,v in error.items():
                messages.error(request, v)
        else:
            new = User.objects.create(
                first = request.POST['reg_first_name'], 
                last = request.POST['reg_last_name'],
                email = request.POST['reg_email'].lower(),
                password = bcrypt.hashpw(request.POST['reg_password'].encode(), bcrypt.gensalt()),
                birthdate = request.POST['reg_birthday'], 
            )
            messages.success(request, f'Welcome {new.first}. Now sign-in!')
        return redirect('/')


def logout(request):
    request.session.clear()
    messages.success(request, 'You have successfully logged out!')
    return redirect('/')


def login(request):
    if request.method == 'GET':
        return redirect('/')
    else:
        error = {}
        User.objects.validate_login(error, request.POST)
        if len(error) > 0:
            for k,v in error.items():
                messages.error(request, v)
        else:
            request.session['user_id'] = User.objects.get(email = request.POST['login_email'].lower()).id
            request.session['user_id'] = User.objects.filter(email = request.POST['login_email'].lower())[0].id
        return redirect('/')

def create_trip(request):
    if request.method == 'GET':
        if 'user_id' not in request.session:
            return redirect('/')
        else:
            return render(request, 'main/create_trip.html')
    else:
        error = {}
        Trip.objects.validate_destination_plan(error, request.POST)
        Trip.objects.validate_date_type(error, request.POST)
        Trip.objects.validate_time_travel(error, request.POST)
        if len(error) > 0:
            prepopulated = {
                'new_destination': request.POST['new_destination'],
                'new_start_date': request.POST['new_start_date'],
                'new_end_date': request.POST['new_end_date'],
                'new_plan': request.POST['new_plan'],
            }
            for k,v in error.items():
                messages.error(request, v)
            return render(request, 'main/create_trip.html', prepopulated)
        else:
            creator = User.objects.get(id=request.session['user_id'])
            trip = Trip.objects.create(
                destination= request.POST['new_destination'],
                start_date= request.POST['new_start_date'],
                end_date= request.POST['new_end_date'],
                plan= request.POST['new_plan'],
                created_by=creator
            )
            trip.attendees.add(creator)
            return redirect('/')
        
def remove_trip(request, trip_id):
    if request.method == 'GET':
        return redirect('/')
    else:
        trip = Trip.objects.get(id=trip_id)
        user = User.objects.get(id=request.session['user_id'])
        user.trips_attending.remove(trip)
        return redirect('/')


        
def edit_trip(request, trip_id):
    if request.method == 'GET':
        user = User.objects.get(id=request.session['user_id'])
        return render(request,'main/edit_trip.html', {'trip': Trip.objects.get(id=trip_id), 'user': user}) 
    else:
        error = {}
        Trip.objects.validate_destination_plan(error, request.POST)
        Trip.objects.validate_date_type(error, request.POST)
        Trip.objects.validate_time_travel(error, request.POST)
        if len(error) > 0:
            for k,v in error.items():
                messages.error(request, v)
            return redirect(f'/trips/edit/{trip_id}')
        else:
            trip = Trip.objects.get(id=trip_id)
            trip.destination = request.POST['new_destination']
            trip.start_date = request.POST['new_start_date']
            trip.end_date = request.POST['new_end_date']
            trip.plan = request.POST['new_plan']
            trip.save()
            return redirect('/')

def add_attendee(request):
    if request.method == 'GET':
        return redirect('/')
    else:
        user = User.objects.get(id = request.session['user_id'])
        trip = Trip.objects.get(id=request.POST['trip_id'])
        user.trips_attending.add(trip)
        return redirect('/')

def cancel_trip(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.session['user_id'])
        trip = Trip.objects.get(id=request.POST['cancel_trip_id'])
        if trip.created_by.id == user.id:
            trip.delete()
    return redirect('/')