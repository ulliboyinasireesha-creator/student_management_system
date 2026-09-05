# Student Management System — Django

A beginner-friendly training project. Departments, courses and students, with
login, search, filters, pagination, photo upload and CSV export.

## Run it

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py seed_data        # 3 departments, 5 courses, 40 students
python manage.py runserver
```

Open http://127.0.0.1:8000/ and log in as **admin / admin123**.
Admin site: http://127.0.0.1:8000/admin/

## Run the tests

```bash
python manage.py test
```

## What is where

| Path | What it holds |
|---|---|
| `config/settings.py` | Settings for the whole project |
| `config/urls.py` | Main address book: admin, login, logout |
| `students/models.py` | Department, Course, Student |
| `students/forms.py` | The three forms and their validation |
| `students/views.py` | Every view function |
| `students/urls.py` | The app's address book |
| `students/admin.py` | Admin site configuration |
| `students/tests.py` | Nine tests |
| `students/management/commands/seed_data.py` | Demo data |
| `templates/base.html` | The page frame every other template extends |
| `students/templates/students/` | One template per page |
| `static/css/style.css` | Styling. Copy it, do not type it. |

## Every view has the same shape

```python
def something_create(request):
    if request.method == 'POST':
        form = SomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('some_list')
    else:
        form = SomeForm()
    return render(request, 'students/some_form.html', {'form': form})
```

Learn this one shape and the rest of the project is repetition.
