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
        projector = False
        name = request.POST.get('name')
        seats = request.POST.get('seats')
        if request.POST.get('projector') == "on":
            projector = True
        Rooms.objects.create(name=name, seats=seats, projector=projector)
        return redirect('home')

