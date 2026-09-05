# A ModelForm builds an HTML form from a model.
# We only tell it: which model, which fields, and how each box should look.

from django import forms
from .models import Course, Department, Student


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student

        fields = [
            'roll_no',
            'first_name',
            'last_name',
            'email',
            'phone',
            'date_of_birth',
            'gender',
            'department',
            'year_of_study',
            'address',
            'admitted_on',
            'photo',
            'is_active',
        ]

        # 'form-control' and 'form-select' are Bootstrap classes.
        # They only change how the box LOOKS.
        widgets = {
            'roll_no': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'year_of_study': forms.NumberInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'admitted_on': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    # ---- Validation ----
    # A method named clean_<fieldname> checks ONE field.

    def clean_roll_no(self):
        roll_no = self.cleaned_data['roll_no']
        roll_no = roll_no.strip().upper()

        if len(roll_no) < 4:
            raise forms.ValidationError('Roll number must be at least 4 characters.')

        return roll_no

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        phone = phone.strip()

        if phone != '':
            if not phone.isdigit() or len(phone) != 10:
                raise forms.ValidationError('Enter a 10 digit phone number.')

        return phone

    # A method named clean() checks TWO OR MORE fields together.

    def clean(self):
        cleaned_data = super().clean()

        date_of_birth = cleaned_data.get('date_of_birth')
        admitted_on = cleaned_data.get('admitted_on')

        if date_of_birth and admitted_on:
            if date_of_birth >= admitted_on:
                raise forms.ValidationError(
                    'Date of birth must be earlier than the admission date.'
                )

        return cleaned_data


class DepartmentForm(forms.ModelForm):

    class Meta:
        model = Department
        fields = ['name', 'code', 'hod_name']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'hod_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = ['name', 'code', 'department', 'semester', 'credits']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'semester': forms.NumberInput(attrs={'class': 'form-control'}),
            'credits': forms.NumberInput(attrs={'class': 'form-control'}),
        }
