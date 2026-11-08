from django.db import models
from django.utils import timezone

from users.models import CustomUser


# Create your models here.
class Building(models.Model):
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    floor_count = models.PositiveIntegerField()
    elevator = models.BooleanField()
    parking = models.BooleanField()
    garage = models.BooleanField()
    cctv = models.BooleanField()
    intercom = models.BooleanField()

    class Meta:
        db_table = "buildings"

    def __str__(self):
        return f"{self.city}, {self.street}"


class Apartment(models.Model):
    unit = models.PositiveIntegerField()
    room_count = models.PositiveIntegerField()
    area = models.PositiveIntegerField()
    floor = models.PositiveIntegerField()
    condition = models.CharField(max_length=255)
    heating = models.CharField(max_length=255)
    furnishings = models.CharField(max_length=255)
    ac = models.BooleanField()
    phone = models.BooleanField()
    television = models.BooleanField()
    internet = models.BooleanField()

    building = models.ForeignKey(Building, related_name="apartments", on_delete=models.CASCADE)

    class Meta:
        db_table = "apartments"

    def get_room_count(self):
        return self.room_count if self.room_count > 0 else "Garsonjera"

    def get_area(self):
        return f"{self.area} m2"

    def get_floor(self):
        floor = self.floor if self.floor > 0 else "Prizemlje"
        return f"{floor}/{self.building.floor_count}"


class Listing(models.Model):
    title = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    move_in_date = models.DateField(default=timezone.now)
    deposit = models.BooleanField()
    for_students = models.BooleanField()
    for_employed = models.BooleanField()
    smoking_allowed = models.BooleanField()
    pets_allowed = models.BooleanField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    apartment = models.ForeignKey(Apartment, related_name="listings", on_delete=models.CASCADE)
    poster = models.ForeignKey(CustomUser, related_name="listings", on_delete=models.CASCADE)

    bookmarks = models.ManyToManyField(CustomUser, db_table="listing_bookmarks", related_name="bookmarked_listings", blank=True)

    class Meta:
        db_table = "listings"

    def get_move_in_date(self):
        comparison = self.move_in_date > self.created_at
        move_in_date = self.move_in_date if comparison else "odmah"
        return f"Useljiv {move_in_date}"

    def is_updated(self):
        return self.updated_at > self.created_at

    def is_bookmarked(self, user: CustomUser):
        return self.bookmarks.contains(user)

    def __str__(self):
        return self.title
