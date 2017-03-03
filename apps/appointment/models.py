from __future__ import unicode_literals
from django.db import models
from ..login.models import User
from datetime import datetime, timedelta


class AppointmentManager(models.Manager):
    # process/create item into Wish

    def add_task(self, date1, time1, task, userid):
        errors = []

        # if len(postData['task']) < 4:
        #     errors.append('item should have more than 3 ch')

        if errors:
            modelResponse = {
                'errors': errors,
                'status': False
            }
        else:
            modelResponse = {
                'status': True
            }
            time = datetime.strptime(time1, "%H:%M")
            date = datetime.strptime(date1, "%Y-%m-%d")

            user = User.userManager.get(id=userid)
            self.create(task=task, time=time,
                        date=date, status='pending', added_by=user,)
            self.add_want(task, userid)

        return modelResponse
    # process/add want into Wish

    def add_want(self, task, userid):
        # create item line 28 add user at 29 by id
        user = User.userManager.get(id=userid)
        tasks = self.filter(task=task)[0]
        tasks.want.add(userid)
        tasks.save()

    def edit(self, task, time, status, date, userid, taskid):
        errors = []

        time1 = datetime.strptime(time, "%H:%M")
        date2 = datetime.strptime(date, "%Y-%m-%d")

        if datetime.strptime(date, "%Y-%m-%d") < datetime.strptime(date, "%Y-%m-%d"):
            errors.append('Invalid date')
        if datetime.strptime(time, "%H:%M") < datetime.strptime(time, "%H:%M"):
            errors.append('Invalid time')
        if len(task) < 1:
            errors.append('tasks needs to have a value')
        if errors:
            modelResponse = {
                'status': False,
                'errors': errors
            }
            return modelResponse

        user = User.userManager.get(id=userid)
        task1 = self.get(id=taskid)
        task1.task = task
        task1.time = time
        task1.date = date
        task1.status = status
        task1.save()
        tasks = self.filter(task=task)[0]
        tasks.want.add(userid)
        tasks.save()

        modelResponse = {
            'status': True
        }
        return modelResponse


class Appointment(models.Model):

    task = models.CharField(max_length=70)
    time = models.TimeField(blank=True)
    date = models.DateField(blank=True)
    status = models.CharField(max_length=70)
    added_by = models.ForeignKey(User, related_name='creator')
    want = models.ManyToManyField(User, related_name="wanted_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    appointmentManager = AppointmentManager()
