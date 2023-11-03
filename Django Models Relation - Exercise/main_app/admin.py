from django.contrib import admin

from main_app.models import Car


# Register your models here.

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("model", "year", "owner", "car_details")

    @staticmethod
    def car_details(obj: Car):
        try:
            owner = obj.owner.name
        except AttributeError:
            owner = "No owner"

        try:
            registration = obj.registration.registration_number
        except AttributeError:
            registration = "No registration number"

        return f"Owner: {owner}, Registration: {registration}"

    car_details.short_description = "Car Details"
