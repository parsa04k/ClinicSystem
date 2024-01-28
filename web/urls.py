from django.urls import path
from . import views

urlpatterns = [
    path("register_patient", views.patient_register_page, name= "register_patient"),
        path("register_employee", views.employee_register_page, name= "register_employee"),
    path("login", views.login_page, name="login"),
    path("home", views.home_page, name="home"),
    path("logout", views.logout_user, name="logout"),
    path("forgot_password", views.forgot_password, name="forgot_password"),
]
