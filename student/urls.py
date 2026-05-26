from django.urls import path
from . import views

urlpatterns = [
    path("", views.student_login, name="student_login"),
    path("dashboard/", views.student_dashboard, name="student_dashboard"),
    path("logout/", views.student_logout, name="student_logout"),  
    path("wallet-help/", views.wallet_help, name='wallet_help'),
    path("<str:reservation_id>/reserve/", views.food_reservation, name="food_reservation"),  
    path("<str:reservation_id>/delete/", views.delete_reservation, name='food_delete'),  
]