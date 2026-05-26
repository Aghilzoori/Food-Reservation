from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path("student/", views.show_list_students, name="student"),
    path('enter_student/', views.enter_student, name="enter_student"),
    path('students/delete/<str:id>/', views.delete_student, name='delete_student'),
    path('student/<str:id>/account/', views.show_account_balance, name='show_account_balance'),
    path('student/<str:id>/increase/', views.inventory_increase, name='inventory_increase'),
    path('student/<str:id>/reduce/', views.inventory_reduction, name='inventory_reduction'),
    path('food/', views.show_list_food, name="food"),
    path('add-food/', views.enter_food, name='add_food'),
    path("food/delete/", views.delete_foods, name="delete_foods"),
    path("reservations/today/", views.admin_reservations_today, name="admin_reservations_today"),
]