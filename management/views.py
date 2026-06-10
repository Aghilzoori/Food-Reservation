from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, DailyFood
from .forms import StudentForms, DailyFoodForms
from student.models import FoodReservation
from datetime import datetime

def home(request):
    return render(request, 'home.html')

def show_list_students(request):
    students = Student.objects.all()
    return render(request, 'student.html', {'students' : students})


def enter_student(request):
    if request.method == "POST":
        form = StudentForms(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('student')
    else:
        form = StudentForms()
    return render(request, "add_student.html")

def delete_student(request, id):
    if request.method == "POST":
        student = get_object_or_404(Student, id=id)
        student.delete()
    return redirect('student')

def show_account_balance(request, id):
    student = get_object_or_404(Student, id=id)
    return render(request, 'account_balance.html', {
        'student': student
    })


def inventory_increase(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        inventory = int(request.POST.get("inventory"))
        inventory_user = int(student.account_balance) + inventory
        student.account_balance = str(inventory_user)
        student.save()

    return redirect('show_account_balance', id=student.id)


def inventory_reduction(request, id):
    student = get_object_or_404(Student, id=id) # یک شرط هست گرفتن شیء یا نمایش  404

    if request.method == "POST":
        inventory = int(request.POST.get("inventory"))
        inventory_user = int(student.account_balance) - inventory
        student.account_balance = str(inventory_user)
        student.save()

    return redirect('show_account_balance', id=student.id)

def show_list_food(request):
    food = DailyFood.objects.all()
    return render(request, 'food.html', {'food':food})

def enter_food(request):
    if request.method == "POST":
        form = DailyFoodForms(request.POST)
        if form.is_valid():
            form.save()
            return redirect("food")
    else:
        form = DailyFoodForms()
    return render(request, 'add_food.html')

def delete_foods(request):
    if request.method == "POST":
        DailyFood.objects.all().delete()
    return redirect('food')


DAY_INT_TO_STR_FA = {
    0: "دوشنبه",
    1: "سه‌شنبه",
    2: "چهارشنبه",
    3: "پنج‌شنبه",
    4: "جمعه",
    5: "شنبه",
    6: "یکشنبه",
}

def admin_reservations_today(request):
    today_weekday = datetime.now().weekday()
    
    day_map = {
        0: 'mon',
        1: 'tue',
        2: 'wed',
        3: 'thu',
        4: 'fri',
        5: 'sat',
        6: 'sun',
    }
    today_code = day_map.get(today_weekday)

    reservations = FoodReservation.objects.filter(food__day=today_code).select_related('student', 'food')

    context = {
        "reservations": reservations,
        "today_name": DAY_INT_TO_STR_FA.get(today_weekday, "امروز")
    }
    return render(request, "admin_reservations_today.html", context)
# Create your views here.
