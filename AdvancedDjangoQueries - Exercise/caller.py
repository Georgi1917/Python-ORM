import os
from datetime import date

import django



# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models

from main_app.models import RealEstateListing, VideoGame, Technology, Project, Programmer, Task

# Create instances of Technology


# Create task instances with custom creation dates


# 1. Get overdue high-priority tasks
overdue_high_priority = Task.overdue_high_priority_tasks()
print("Overdue High Priority Tasks:")
for task in overdue_high_priority:
    print('- ' + task.title)



