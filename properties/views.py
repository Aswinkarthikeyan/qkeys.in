from django.shortcuts import render

def home(request):
    locations = Location.objects.all()
    bhks = BHKType.objects.all()

    print("Locations:", locations)
    print("BHK:", bhks)

    return render(request, "index.html", {
        "locations": locations,
        "bhks": bhks,
    })

def about(request):
    return redirect(request, "aboutus.html")

def contact(request):
    return redirect(request, "contactus.html")

from .models import BHKType

def bhk(request):
    bhks = BHKType.objects.all()

    return render(request, "bhk.html", {
        "bhks": bhks
    })

from .models import Location

def location(request):

    locations = Location.objects.all()

    return render(request,
                  "location.html",
                  {
                      "locations": locations
                  })

from .models import Property

def properties_by_bhk(request, bhk_id):

    properties = Property.objects.filter(
        bhk_id=bhk_id
    )

    return render(
        request,
        "properties.html",
        {
            "properties": properties
        }
    )
    
def properties_by_location(request, location_id):

    properties = Property.objects.filter(
        location_id=location_id
    )

    return render(
        request,
        "properties.html",
        {
            "properties": properties
        }
    )
    
from django.shortcuts import get_object_or_404


def property_detail(request, id):

    property = get_object_or_404(Property, id=id)

    return render(
        request,
        "property_detail.html",
        {
            "property": property
        }
    )
    

def property_detail(request, id):

    property = get_object_or_404(Property, id=id)

    return render(
        request,
        "property_detail.html",
        {
            "property": property
        }
    )
    
from .models import Property

def search_properties(request):

    location = request.GET.get("location")

    bhk = request.GET.get("bhk")

    properties = Property.objects.all()

    if location:
        properties = properties.filter(location_id=location)

    if bhk:
        properties = properties.filter(bhk_id=bhk)

    return render(
        request,
        "properties.html",
        {
            "properties": properties,
        },
    )
    
from .models import Property

def all_properties(request):

    properties = Property.objects.all()

    return render(
        request,
        "properties.html",
        {
            "properties": properties,
        },
    )
    
TIME_SLOTS = [
    "10-12 AM",
    "12-2 PM",
    "2-4 PM",
    "4-6 PM"
]

def contact(request):

    bhks = BHKType.objects.all()

    available_slots = TIME_SLOTS

    return redirect(
        request,
        "contactus.html",
        {
            "bhks": bhks,
            "available_slots": available_slots,
        }
    )
    
from urllib.parse import quote

from django.shortcuts import render, redirect

from .models import *

from urllib.parse import quote
from django.shortcuts import render, redirect

def contact(request):

    if request.method == "POST":

        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        purpose = request.POST.get("purpose")
        bhk = request.POST.get("bhk")
        visit_date = request.POST.get("visit_date")
        visit_time = request.POST.get("visit_time")
        message = request.POST.get("message")

        # Save to database
        ContactInquiry.objects.create(
            name=name,
            phone=phone,
            email=email,
            purpose=purpose,
            bhk_id=bhk,
            visit_date=visit_date,
            visit_time=visit_time,
            message=message
        )

        whatsapp_message = f"""
🏠 SITE VISIT ENQUIRY

Name: {name}
Phone: {phone}
Email: {email}
Purpose: {purpose}
BHK: {bhk}
Visit Date: {visit_date}
Visit Time: {visit_time}

Message:
{message}
"""

        whatsapp_url = (
            "https://wa.me/918438383770?text="
            + quote(whatsapp_message)
        )

        return redirect(whatsapp_url)

    bhks = BHKType.objects.all()

    available_slots = [
        "10-12 AM",
        "12-2 PM",
        "2-4 PM",
        "4-6 PM",
    ]

    return render(request, "contactus.html", {
        "bhks": bhks,
        "available_slots": available_slots,
    })