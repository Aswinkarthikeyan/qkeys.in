from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path("bhk/", views.bhk, name="bhk"),

path("location/", views.location, name="location"),

path("bhk/<int:bhk_id>/",
     views.properties_by_bhk,
     name="properties_by_bhk"),

path("location/<int:location_id>/",
     views.properties_by_location,
     name="properties_by_location"),

path("property/<int:id>/",
     views.property_detail,
     name="property_detail",
     ),

path(
    "search/",
    views.search_properties,
    name="search_properties",
),


path(
    "property/<int:id>/",
    views.property_detail,
    name="property_detail"
),

path(
    "properties/",
    views.all_properties,
    name="all_properties",
),

path(
    "contact/",
    views.contact,
    name="contact"
)
]


