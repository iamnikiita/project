# from django.shortcuts import render
# from accounts.models import *
# from django.http import HttpResponseRedirect
# import hmac
# import hashlib
# import base64
# import uuid

# def genSha256(key, message):
#         key = key.encode('utf-8')
#         message = message.encode('utf-8')

#         hmac_sha256 = hmac.new(key, message, hashlib.sha256)
#         digest = hmac_sha256.digest()

#         signature = base64.b64encode(digest).decode('utf-8')

#         return signature

#         return signature
# def index(request):
#     movies = Movie.objects.all().order_by('-movie_rating')
#     context = {
#         'mov': movies
#     }
#     return render(request,"index.html", context)

# def movies(request, id):
#     movies = Movie.objects.get(movie=id)
#     cin = Cinema.objects.filter(cinema_show__movie=movies).prefetch_related('cinema_show').distinct()
#     show = Shows.objects.filter(movie=id)
#     context = {
#         'movies': movies,
#         'show': show,
#         'cin': cin,
#     }
#     return render(request, "movies.html", context)

# def seat(request, id):
#     show = Shows.objects.get(shows=id)
#     seat = Bookings.objects.filter(shows=id)
#     return render(request,"seat.html", {'show': show, 'seat': seat})

# def booked(request):
#     if request.method == 'POST':
#         user = request.user
#         seat = ','.join(request.POST.getlist('check'))
#         show = request.POST['show']
#         book = Bookings(useat=seat, shows_id=show, user=user)
#         book.save()
#         return render(request,"booked.html", {'book': book})

# def ticket(request, id):
#     ticket = Bookings.objects.get(id=id)
#     selected_seats = ticket.useat.split(',')  # List of selected seats
#     total_price = len(selected_seats) * ticket.shows.price
#     print(total_price)
#     secret_key = "8gBm/:&EnhH.1/q"
#     uuid_val = uuid.uuid4()
#     data_to_sign = f"total_amount={total_price},transaction_uuid={uuid_val},product_code=EPAYTEST"
#     result = genSha256(secret_key, data_to_sign)
#     context = {
#         'ticket': ticket,
#         'total_price': total_price,
#         'uuid':uuid_val,
#         'signature':result,


#     }

#     return render(request, "ticket.html", context)


from django.shortcuts import render, redirect
from accounts.models import *
from django.http import HttpResponseRedirect, JsonResponse
import hmac
import hashlib
import base64
import uuid
from django.contrib.sessions.backends.db import SessionStore
from django.views.decorators.csrf import csrf_exempt

def genSha256(key, message):
    key = key.encode('utf-8')
    message = message.encode('utf-8')
    hmac_sha256 = hmac.new(key, message, hashlib.sha256)
    digest = hmac_sha256.digest()
    signature = base64.b64encode(digest).decode('utf-8')
    return signature

<<<<<<< HEAD
=======
        hmac_sha256 = hmac.new(key, message, hashlib.sha256)
        digest = hmac_sha256.digest()

        signature = base64.b64encode(digest).decode('utf-8')
        return signature
>>>>>>> 3599d1e97897760c837533113beafe5e812f8909
def index(request):
    movies = Movie.objects.all().order_by('-movie_rating')
    return render(request, "index.html", {'mov': movies})

def booked(request):
    if request.method == 'POST':
        user = request.user
        seat = ','.join(request.POST.getlist('check'))
        show = request.POST['show']
        book = Bookings(useat=seat, shows_id=show, user=user)
        book.save()
        return render(request,"booked.html", {'book': book})


def movies(request, id):
    movies = Movie.objects.get(movie=id)
    cin = Cinema.objects.filter(cinema_show__movie=movies).prefetch_related('cinema_show').distinct()
    show = Shows.objects.filter(movie=id)
    return render(request, "movies.html", {
        'movies': movies,
        'show': show,
        'cin': cin,
    })

def seat(request, id):
    show = Shows.objects.get(shows=id)
    booked_seats = Bookings.objects.filter(shows=id, payment_status='completed')
    
    # Create a list of all booked seat numbers
    occupied_seats = []
    for booking in booked_seats:
        # Split the useat string into individual seat numbers and clean them
        seats = [seat.strip() for seat in booking.useat.split(',') if seat.strip()]
        # Remove any '#' from the beginning of seat numbers if present
        seats = [seat[1:] if seat.startswith('#') else seat for seat in seats]
        occupied_seats.extend(seats)
    
    return render(request, "seat.html", {
        'show': show, 
        'occupied_seats': occupied_seats
    })

def initiate_booking(request):
    if request.method == 'POST':
        selected_seats = request.POST.getlist('check')
        show_id = request.POST['show']
        
        # Store booking details in session
        request.session['pending_booking'] = {
            'seats': selected_seats,
            'show_id': show_id,
        }
        
        # Calculate total price
        show = Shows.objects.get(shows=show_id)
        total_price = len(selected_seats) * show.price
        
        # Generate payment details
        transaction_uuid = str(uuid.uuid4())
        secret_key = "8gBm/:&EnhH.1/q"
        data_to_sign = f"total_amount={total_price},transaction_uuid={transaction_uuid},product_code=EPAYTEST"
        signature = genSha256(secret_key, data_to_sign)
        
        return render(request, "ticket.html", {
            'total_price': total_price,
            'uuid': transaction_uuid,
            'signature': signature,
            'selected_seats': ','.join(selected_seats),
            'show': show,
        })

@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        pending_booking = request.session.get('pending_booking')
        if pending_booking:
            user = request.user
            seat = ','.join(pending_booking['seats'])
            show_id = pending_booking['show_id']
            
            # Create booking with completed status
            booking = Bookings(
                user=user,
                shows_id=show_id,
                useat=seat,
                payment_status='completed'  # Set status to completed
            )
            booking.save()
            
            # Clear session
            del request.session['pending_booking']
            
            return redirect('ticket', id=booking.id)
    return HttpResponseRedirect('/')

def ticket(request, id):
    ticket = Bookings.objects.get(id=id, payment_status='completed')
    selected_seats = ticket.useat.split(',')
    total_price = len(selected_seats) * ticket.shows.price
    
    return render(request, "ticket.html", {
        'ticket': ticket,
        'total_price': total_price,
    })