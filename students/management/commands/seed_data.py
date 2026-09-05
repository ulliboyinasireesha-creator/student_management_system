# Demo data, so we never have to type 40 students by hand.
# Run it with:  python manage.py seed_data

import random
from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from students.models import Course, Department, Student

FIRST_NAMES = ['Murali', 'Anusha', 'Kiran', 'Sravani', 'Rahul', 'Divya',
               'Praveen', 'Harika', 'Naveen', 'Lakshmi', 'Sai', 'Bhavana',
               'Vamsi', 'Keerthi', 'Arjun', 'Sneha', 'Rohit', 'Pooja']

LAST_NAMES = ['Reddy', 'Naidu', 'Sharma', 'Rao', 'Chowdary', 'Kumar', 'Varma']

DEPARTMENTS = [
    ['Computer Science and Engineering', 'CSE', 'Dr. S. Ramesh'],
    ['Electronics and Communication', 'ECE', 'Dr. K. Padmaja'],
    ['Mechanical Engineering', 'MECH', 'Dr. B. Anand'],
]

COURSES = [
    ['Database Management Systems', 'CS301', 'CSE', 3, 4],
    ['Operating Systems', 'CS302', 'CSE', 3, 4],
    ['Web Technologies', 'CS303', 'CSE', 3, 3],
    ['Digital Signal Processing', 'EC301', 'ECE', 3, 4],
    ['Thermodynamics', 'ME201', 'MECH', 2, 4],
]


class Command(BaseCommand):
    help = 'Load demo departments, courses and students.'

    def handle(self, *args, **options):
        random.seed(42)          # same demo data every time

        # 1. Create a login for ourselves
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write('Created superuser  admin / admin123')

        # 2. Departments
        departments = {}
        for name, code, hod in DEPARTMENTS:
            dept, created = Department.objects.get_or_create(
                code=code,
                defaults={'name': name, 'hod_name': hod},
            )
            departments[code] = dept

        # 3. Courses
        for name, code, dept_code, semester, credits in COURSES:
            Course.objects.get_or_create(
                code=code,
                defaults={
                    'name': name,
                    'department': departments[dept_code],
                    'semester': semester,
                    'credits': credits,
                },
            )

        # 4. Students
        today = timezone.now().date()
        for number in range(1, 41):
            dept_code = random.choice(['CSE', 'ECE', 'MECH'])
            first = random.choice(FIRST_NAMES)
            last = random.choice(LAST_NAMES)

            Student.objects.get_or_create(
                roll_no='23' + dept_code + str(number).zfill(3),
                defaults={
                    'first_name': first,
                    'last_name': last,
                    'email': first.lower() + '.' + last.lower() + str(number) + '@college.edu',
                    'phone': '9' + str(random.randint(100000000, 999999999)),
                    'gender': random.choice(['M', 'F']),
                    'department': departments[dept_code],
                    'year_of_study': random.randint(1, 4),
                    'address': 'Nellore, Andhra Pradesh',
                    'date_of_birth': today - timedelta(days=random.randint(6600, 7600)),
                    'admitted_on': today - timedelta(days=random.randint(200, 1400)),
                    'is_active': random.random() > 0.1,
                },
            )

        self.stdout.write('Departments: ' + str(Department.objects.count()))
        self.stdout.write('Courses:     ' + str(Course.objects.count()))
        self.stdout.write('Students:    ' + str(Student.objects.count()))
