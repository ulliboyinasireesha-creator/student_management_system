# The main address book for the whole project.

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),

    # Django gives us the login and logout logic for free.
    path('accounts/login/',
         auth_views.LoginView.as_view(template_name='registration/login.html'),
         name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Send everything else to our app's address book.
    path('', include('students.urls')),
]

# While DEBUG is True, let Django serve the uploaded photos.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
