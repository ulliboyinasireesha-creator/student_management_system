# Every view below follows the SAME shape.
# Learn one, and you know them all.

import csv

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CourseForm, DepartmentForm, StudentForm
from .models import Course, Department, Student


@login_required
def dashboard(request):

    # annotate() adds a calculated column to each row. It is SQL GROUP BY.
    departments = Department.objects.annotate(count=Count('students'))

    return render(request, 'students/dashboard.html', {
        'total_students': Student.objects.filter(is_active=True).count(),
        'total_inactive': Student.objects.filter(is_active=False).count(),
        'total_departments': Department.objects.count(),
        'total_courses': Course.objects.count(),
        'departments': departments,
        'recent_students': Student.objects.order_by('-created_at')[:5],
    })


def about(request):
    return render(request, 'students/about.html')


def contact(request):
    return render(request, 'students/contact.html')


# ---------------- students ----------------

@login_required
def student_list(request):

    # select_related fetches each student's department in the SAME query.
    # Without it, 40 students = 41 database queries.
    students = Student.objects.select_related('department')

    # 1. Read what the user typed in the search box.
    search = request.GET.get('q', '')
    search = search.strip()

    if search != '':
        # Q objects let us say "match roll_no OR first_name OR last_name OR email".
        students = students.filter(
            Q(roll_no__icontains=search)
            | Q(first_name__icontains=search)
            | Q(last_name__icontains=search)
            | Q(email__icontains=search)
        )

    # 2. Read the two dropdowns.
    selected_department = 0
    department_id = request.GET.get('department', '')
    if department_id.isdigit():
        selected_department = int(department_id)
        students = students.filter(department_id=selected_department)

    selected_year = 0
    year = request.GET.get('year', '')
    if year.isdigit():
        selected_year = int(year)
        students = students.filter(year_of_study=selected_year)

    # 3. Show 10 per page.
    paginator = Paginator(students, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 4. Keep the search and filters when the user clicks "Next".
    extra_query = ''
    if search != '':
        extra_query = extra_query + '&q=' + search
    if selected_department != 0:
        extra_query = extra_query + '&department=' + str(selected_department)
    if selected_year != 0:
        extra_query = extra_query + '&year=' + str(selected_year)

    return render(request, 'students/student_list.html', {
        'page_obj': page_obj,
        'departments': Department.objects.all(),
        'search': search,
        'selected_department': selected_department,
        'selected_year': selected_year,
        'total_found': paginator.count,
        'extra_query': extra_query,
    })


@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'students/student_detail.html', {'student': student})


@login_required
def student_create(request):

    if request.method == 'POST':
        # request.FILES is needed because the form has a photo field.
        form = StudentForm(request.POST, request.FILES)

        if form.is_valid():
            student = form.save()
            messages.success(request, 'Added ' + student.full_name() + '.')
            return redirect('student_list')
        else:
            messages.error(request, 'Please fix the errors below.')

    else:
        form = StudentForm()

    return render(request, 'students/student_form.html', {
        'form': form,
        'title': 'Add student',
        'button_label': 'Save student',
    })


@login_required
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        # instance=student is the ONLY difference from student_create.
        form = StudentForm(request.POST, request.FILES, instance=student)

        if form.is_valid():
            form.save()
            messages.success(request, 'Updated ' + student.full_name() + '.')
            return redirect('student_detail', pk=student.pk)
        else:
            messages.error(request, 'Please fix the errors below.')

    else:
        form = StudentForm(instance=student)

    return render(request, 'students/student_form.html', {
        'form': form,
        'title': 'Edit ' + student.roll_no,
        'button_label': 'Save changes',
    })


@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        name = student.full_name()
        student.delete()
        messages.success(request, 'Deleted ' + name + '.')
        return redirect('student_list')

    return render(request, 'students/confirm_delete.html', {'student': student})


# ---------------- departments ----------------

@login_required
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'students/department_list.html', {'departments': departments})


@login_required
def department_create(request):

    if request.method == 'POST':
        form = DepartmentForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Department added.')
            return redirect('department_list')
        else:
            messages.error(request, 'Please fix the errors below.')

    else:
        form = DepartmentForm()

    return render(request, 'students/simple_form.html', {
        'form': form,
        'title': 'Add department',
        'button_label': 'Save department',
        'cancel_url': 'department_list',
    })


# ---------------- courses ----------------

@login_required
def course_list(request):
    courses = Course.objects.select_related('department')
    return render(request, 'students/course_list.html', {'courses': courses})


@login_required
def course_create(request):

    if request.method == 'POST':
        form = CourseForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Course added.')
            return redirect('course_list')
        else:
            messages.error(request, 'Please fix the errors below.')

    else:
        form = CourseForm()

    return render(request, 'students/simple_form.html', {
        'form': form,
        'title': 'Add course',
        'button_label': 'Save course',
        'cancel_url': 'course_list',
    })


# ---------------- export ----------------

@login_required
def student_export_csv(request):
    # This view returns a FILE, not a page. It uses no template at all.

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'

    writer = csv.writer(response)
    writer.writerow(['Roll No', 'Name', 'Email', 'Phone', 'Department', 'Year', 'Active'])

    for student in Student.objects.select_related('department'):
        writer.writerow([
            student.roll_no,
            student.full_name(),
            student.email,
            student.phone,
            student.department.code,
            student.year_of_study,
            student.is_active,
        ])

    return response
