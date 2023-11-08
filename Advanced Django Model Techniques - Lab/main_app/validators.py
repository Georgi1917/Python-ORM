from django.core.exceptions import ValidationError


def validate_menu_categories(desc):
    NEEDED_CATEGORIES = [
        "Appetizers",
        "Main Course",
        "Desserts",
    ]

    for category in NEEDED_CATEGORIES:
        if category not in desc:
            raise ValidationError('The menu must include each of the categories "Appetizers", "Main Course", "Desserts".')