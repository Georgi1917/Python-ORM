import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

# Create queries within functions

from main_app import models

print(models.Shoe.objects.all().values_list('brand', flat=True).distinct())
order_model = models.Order

print(order_model.objects.all().filter(status='Cll').delete())
