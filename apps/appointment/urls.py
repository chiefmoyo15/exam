from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^$", views.index, name="index"),
    url(r"^(?P<taskid>\d+)$", views.edit, name="edit"),
    url(r"^process$", views.process, name="process"),
    url(r"^item/(?P<taskid>\d+)$", views.item, name="item"),
    url(r'^delete/(?P<taskid>\d+)$', views.delete, name='delete'),

]
