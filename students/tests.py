# Tests are small programs that check our program.
# Run them with:  python manage.py test

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Course, Department, Student


class StudentModelTests(TestCase):

    def setUp(self):
        # setUp runs before EVERY test below, on a fresh empty database.
        self.department = Department.objects.create(
            name='Computer Science', code='CSE'
        )
        self.student = Student.objects.create(
            roll_no='23CSE001',
            first_name='Ravi',
            last_name='Kumar',
            email='ravi@college.edu',
            department=self.department,
        )

    def test_full_name(self):
        self.assertEqual(self.student.full_name(), 'Ravi Kumar')

    def test_str_shows_roll_no(self):
        self.assertIn('23CSE001', str(self.student))

    def test_department_counts_its_students(self):
        self.assertEqual(self.department.student_count(), 1)

    def test_reverse_lookup_works(self):
        self.assertIn(self.student, self.department.students.all())


class StudentPageTests(TestCase):

    def setUp(self):
        self.department = Department.objects.create(
            name='Computer Science', code='CSE'
        )
        User.objects.create_user(username='staff', password='pass12345')

    def test_student_list_needs_login(self):
        response = self.client.get(reverse('student_list'))
        self.assertEqual(response.status_code, 302)      # redirected to login

    def test_student_list_works_after_login(self):
        self.client.login(username='staff', password='pass12345')
        response = self.client.get(reverse('student_list'))
        self.assertEqual(response.status_code, 200)

    def test_can_add_a_student(self):
        self.client.login(username='staff', password='pass12345')
        self.client.post(reverse('student_create'), {
            'roll_no': '23CSE009',
            'first_name': 'Anu',
            'last_name': 'Rao',
            'email': 'anu@college.edu',
            'phone': '9876543210',
            'gender': 'F',
            'department': self.department.id,
            'year_of_study': 2,
            'address': 'Nellore',
            'admitted_on': '2023-08-01',
            'is_active': True,
        })
        self.assertEqual(Student.objects.count(), 1)

    def test_short_roll_number_is_rejected(self):
        self.client.login(username='staff', password='pass12345')
        self.client.post(reverse('student_create'), {
            'roll_no': 'AB',
            'first_name': 'Anu',
            'last_name': 'Rao',
            'email': 'anu2@college.edu',
            'gender': 'F',
            'department': self.department.id,
            'year_of_study': 1,
            'admitted_on': '2023-08-01',
        })
        self.assertEqual(Student.objects.count(), 0)


class CourseTests(TestCase):

    def setUp(self):
        self.department = Department.objects.create(
            name='Computer Science', code='CSE'
        )
        User.objects.create_user(username='staff', password='pass12345')

    def test_course_shows_in_the_list(self):
        Course.objects.create(
            name='Operating Systems', code='CS302',
            department=self.department, semester=3,
        )
        self.client.login(username='staff', password='pass12345')
        response = self.client.get(reverse('course_list'))
        self.assertContains(response, 'CS302')
