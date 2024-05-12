from datetime import datetime, date

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from myapp.models import Rooms, RoomsReservation


# Create your views here.

class HomePage(View):
    def get(self, request):
        rooms = Rooms.objects.all()
        if len(rooms) == 0:
            message = "No rooms in DB"
            return render(request, 'home_page.html', {'message': message,
                                                      'today': date.today()})
        for room in rooms:
            reservation_dates = [i.date for i in RoomsReservation.objects.filter(room=room.id)]
            room.reserved = date.today() in reservation_dates
        return render(request, 'home_page.html', {'rooms': rooms,
                                                  'today': date.today()})


    def post(self, request):
        search = request.POST.get('search')
        rooms_search = Rooms.objects.filter(name=search)
        if len(rooms_search) == 0:
            message = "no such room"
            return render(request, 'home_page.html', {'message': message,
                                                      'today': date.today()})

        return render(request, 'home_page.html', {'rooms': rooms_search,
                                                  'today': date.today()})

class AddRoom(View):
    def get(self, request):
        return render(request, 'add_room.html')

    def post(self, request):
        error = ""
        name = request.POST.get('name')
        seats = request.POST.get('seats')
        projector = request.POST.get('projector') == 'on'
        if len(name) not in range(1, 50):
            error += " Name must be between 1 and 50 characters, "
        for i in Rooms.objects.all():
            if i.name == name:
                error += " Room of this name already exists, "
        if int(seats) < 0:
            error += "seats number must be not negative"

        if len(error) > 0:
            return render(request, 'add_room.html', {'error': error})

        Rooms.objects.create(name=name, seats=seats, projector=projector)
        return redirect('home')


class EditRoom(View):

    def get(self, request, pk):
        room = Rooms.objects.get(pk=pk)
        return render(request, 'add_room.html', {'room': room})

    def post(self, request, pk):
        error = ""
        room = Rooms.objects.get(pk=pk)
        name = request.POST.get('name')
        seats = request.POST.get('seats')
        projector = request.POST.get('projector') == 'on'
        if len(name) not in range(1, 50):
            error += " Name must be between 1 and 50 characters, "
        for i in Rooms.objects.all():
            if i.name == name and name != room.name:
                error += " Room of this name already exists, "
        if int(seats) < 0:
            error += "seats number must be not negative"

        if len(error) > 0:
            return render(request, 'add_room.html', {'error': error})
        room.name = name
        room.seats = seats
        room.projector = projector
        room.save()
        return redirect(f'/home/room/{pk}')


class DeleteRoom(View):
    def get(self, request, pk):
        Rooms.objects.filter(id=pk).delete()
        return redirect('home')


class RoomsView(View):
    def get(self, request, pk):
        room = Rooms.objects.get(pk=pk)
        reservations = RoomsReservation.objects.filter(room=room)
        if len(RoomsReservation.objects.filter(room=room, date=date.today())) == 1:
            today_occupied = "occupied"
        else:
            today_occupied = "Free"
        return render(request, 'room_view.html', {'room': room,
                                                  'reservations': reservations,
                                                  'today_occupied': today_occupied})

    def post(self, request, pk):

        room = Rooms.objects.get(pk=pk)
        reservations = RoomsReservation.objects.filter(room=room)
        if len(RoomsReservation.objects.filter(room=room, date=date.today())) == 1:
            today_occupied = "occupied"
        else:
            today_occupied = "unoccupied"

        reservation_date = request.POST.get('date')
        room = Rooms.objects.get(pk=pk)
        if str(date.today()) > reservation_date:
            reservations = RoomsReservation.objects.filter(room=room)
            message = "date must be in future"
            return render(request, 'room_view.html', {'room': room, 'reservations': reservations,
                                                      'message': message,
                                                      'today_occupied': today_occupied})
        if len(RoomsReservation.objects.filter(room=room, date=reservation_date)) > 0:
            reservations = RoomsReservation.objects.filter(room=room)
            message = "date already taken"
            return render(request, 'room_view.html', {'room': room, 'reservations': reservations,
                                                      'message': message,
                                                      'today_occupied': today_occupied})
        RoomsReservation.objects.create(room=room, date=reservation_date, comment="na razie nie ma commenta")
        return redirect(f'/home/room/{room.id}')
