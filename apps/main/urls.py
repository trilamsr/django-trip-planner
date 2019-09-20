from django.conf.urls import url
from . import views

urlpatterns = [
# get
    url(r"^dashboard/?$", views.reroute),
    url(r"^trips/?$", views.reroute),
    url(r"^$", views.main),

# post
    url(r"^register/?$", views.register),
    url(r"^logout/?$", views.logout),
    url(r"^login/?$", views.login),
    url(r"^trips/remove/(?P<trip_id>\d+)/?$", views.remove_trip),
    url(r"^add_attendee/?$", views.add_attendee),
    url(r"^cancel_trip/?$", views.cancel_trip),



# double-threat
    url(r"^create_trip/?$", views.create_trip),
    url(r"^trips/edit/(?P<trip_id>\d+)?$", views.edit_trip),
]