from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class BHKType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Amenity(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Property(models.Model):

    AVAILABILITY = (
        ('Available', 'Available'),
        ('Sold Out', 'Sold Out'),
    )

    title = models.CharField(max_length=200)

    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE
    )

    bhk = models.ForeignKey(
        BHKType,
        on_delete=models.CASCADE
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    area = models.IntegerField(
        help_text="Area in Sq.ft"
    )

    bedrooms = models.IntegerField()

    bathrooms = models.IntegerField()

    parking = models.BooleanField(default=True)

    facing = models.CharField(max_length=50)

    availability = models.CharField(
        max_length=20,
        choices=AVAILABILITY,
        default='Available'
    )

    description = models.TextField()

    amenities = models.ManyToManyField(Amenity)

    image = models.ImageField(
        upload_to='properties/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class ContactInquiry(models.Model):

    name = models.CharField(max_length=100)

    phone = models.CharField(max_length=15)

    email = models.EmailField(blank=True)

    purpose = models.CharField(max_length=100)

    bhk = models.ForeignKey(
        BHKType,
        on_delete=models.SET_NULL,
        null=True
    )

    visit_date = models.DateField()

    visit_time = models.CharField(max_length=20)

    message = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name