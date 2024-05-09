from django.shortcuts import render, redirect
from django.views import View

from myapp.models import Rooms


# Create your views here.

class HomePage(View):
    def get(self, request):
        return render(request, 'home_page.html', {'rooms': Rooms.objects.all()})

    def post(self, request):
        pass


class AddRoom(View):
    def get(self, request):
        return render(request, 'add_room.html')

    def post(self, request):
        name = request.POST.get('name')
        seats = request.POST.get('seats')
        projector = request.POST.get('projector') == 'on'
        Rooms.objects.create(name=name, seats=seats, projector=projector)
        return redirect('home')


class EditRoom(View):

    def get(self, request, pk):
        room = Rooms.objects.get(pk=pk)
        return render(request, 'add_room.html', {'room': room})

    def post(self, request, pk):

        room = Rooms.objects.get(pk=pk)
        name = request.POST.get('name')
        seats = request.POST.get('seats')
        projector = request.POST.get('projector') == 'on'
        room.name = name
        room.seats = seats
        room.projector = projector
        room.save()
        return redirect('home')

class DeleteRoom(View):
    def get(self, request, pk):
        Rooms.objects.filter(id=pk).delete()
        return redirect('home')


