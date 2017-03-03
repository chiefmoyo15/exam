from django.shortcuts import render, HttpResponse, redirect
from .models import User
from django.contrib import messages
from django.contrib.messages import get_messages
import re
import bcrypt


def index(request):
    # if request.session['isLoggedin'] == True:
    #     return redirect('/show')
    context = {
        'all': User.userManager.all()
    }

    return render(request, 'login/index.html', context)


# def user_name(self, id):
#     name = self.get(id=id)
#     return name.first_name


def login(request):

    response_from_models = User.userManager.login(request.POST)
    if response_from_models['status']:
        # status is true, sending to success page
        request.session['userid'] = response_from_models['userid']
        request.session['name'] = response_from_models['name']
        # request.session['userid'] = response_from_models['userid']
        return redirect('appointment:index')
    else:
        messages.add_message(request, messages.ERROR,
                             response_from_models['error'])
        return redirect('home:index')
    return render(request, "appoinment/index.html")


def register(request):
    if request.method == "POST":
        response_from_models = User.userManager.register(request.POST['first_name'], request.POST[
            'last_name'], request.POST['email'], request.POST['password'], request.POST['password2'], request.POST['dateHired'])
        if not response_from_models['status']:
            for error in response_from_models['errors']:
                messages.add_message(request, messages.ERROR, error)
            return redirect('/')
    request.session['userid'] = response_from_models['userid']
    request.session['name'] = response_from_models['name']
    return redirect('appointment:index')


def success(request):
    if 'email' in request.session:
        messages.error(request, 'Must be logged in to continue')
        return redirect('home:index')
    return render(request, 'login/show.html')


def logout(request):
    request.session.clear()
    return redirect('/')
