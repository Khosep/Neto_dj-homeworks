import csv

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse

from pagination.settings import BUS_STATION_CSV


def index(request):
    return redirect(reverse('bus_stations')+'?page=1')


def bus_stations(request):
    with open(BUS_STATION_CSV, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        bus_stations_list = [obj for obj in reader]

    page_number = int(request.GET.get("page", 1))
    paginator = Paginator(bus_stations_list, 10)
    page_obj = paginator.get_page(page_number)
    context = {
        'bus_stations': page_obj,
        'page': page_obj
    }
    return render(request, 'stations/index.html', context)
