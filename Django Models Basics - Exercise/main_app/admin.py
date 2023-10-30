from django.contrib import admin

# Register your models here.

from main_app.models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass
