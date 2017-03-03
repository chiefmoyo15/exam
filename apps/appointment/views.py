from django.shortcuts import render, HttpResponse, redirect
from .models import Appointment
from ..login.models import User
from django.contrib import messages
from django.contrib.messages import get_messages
from datetime import datetime, timedelta, date


def index(request):
    if 'userid' not in request.session:
        return redirect('home:index')
    today = datetime.now()
    context = {
        'tasklist': Appointment.appointmentManager.filter(want=request.session['userid'], date__lte=datetime.now()).order_by('time'),
        'tasklist2': Appointment.appointmentManager.filter(want=request.session['userid'], date__gt=datetime.now()),
        'date': datetime.now()
    }
    return render(request, 'appointment/index.html', context)


def item(request, taskid):
    if 'userid' not in request.session:
        return redirect('home:index')

    response_from_models = Appointment.appointmentManager.edit(request.POST['task'], request.POST['time'], request.POST[
        'status'], request.POST['date'], request.session['userid'], taskid)

    if not response_from_models['status']:
        for error in response_from_models['errors']:
            messages.add_message(request, messages.ERROR, error)

    return redirect('appointment:index')


def process(request):
    response_from_models = Appointment.appointmentManager.add_task(
        request.POST['date'], request.POST['time'], request.POST['task'], request.session['userid'])
    if not response_from_models['status']:
        for error in response_from_models['errors']:
            messages.add_message(request, messages.ERROR, error)

    return redirect('appointment:index')

#
#


def edit(request, taskid):
    if 'userid' not in request.session:
        return redirect('home:index')
    context = {
        'task': Appointment.appointmentManager.get(id=taskid)
    }
    return render(request, 'appointment/edit.html', context)


def delete(request, taskid):
    if 'userid' not in request.session:
        return redirect('home:index')
    Appointment.delete(Appointment.appointmentManager.get(id=taskid))
    return redirect('appointment:index')
