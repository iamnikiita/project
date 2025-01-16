from django.shortcuts import render
from accounts.models import *
from django.http import HttpResponseRedirect

def index(request):
    movies = Movie.objects.all().order_by('-movie_rating')
    context = {
        'mov': movies
    }
    return render(request,"index.html", context)

def movies(request, id):
    movies = Movie.objects.get(movie=id)
    cin = Cinema.objects.filter(cinema_show__movie=movies).prefetch_related('cinema_show').distinct()
    show = Shows.objects.filter(movie=id)
    context = {
        'movies': movies,
        'show': show,
        'cin': cin,
    }
    return render(request, "movies.html", context)

def seat(request, id):
    show = Shows.objects.get(shows=id)
    seat = Bookings.objects.filter(shows=id)
    return render(request,"seat.html", {'show': show, 'seat': seat})

def booked(request):
    if request.method == 'POST':
        user = request.user
        seat = ','.join(request.POST.getlist('check'))
        show = request.POST['show']
        book = Bookings(useat=seat, shows_id=show, user=user)
        book.save()
        return render(request,"booked.html", {'book': book})

def ticket(request, id):
    ticket = Bookings.objects.get(id=id)
    selected_seats = ticket.useat.split(',')  # List of selected seats
    total_price = len(selected_seats) * ticket.shows.price
    context = {
        'ticket': ticket,
        'total_price': total_price
    }
    return render(request, "ticket.html", context)
