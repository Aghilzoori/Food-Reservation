from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, DailyFood
from .forms import StudentForms, DailyFoodForms
from student.models import FoodReservation
from datetime import datetime
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def login_user(request):
    context = {}
    
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user:
            
            login(request, user)
            
            return redirect('home')
        context['error'] = 'رمز یا نام حساب کاربری اشتباه است'
        return render(request, 'login.html', context)
    
    return render(request, "login.html")

def logout_user(request):
    logout(request)
    messages.info(request, "شما از حساب کاربری خارج شدین")
    return redirect("login")

def home(request):
    return render(request, 'home.html')
@login_required(login_url="login")
def show_list_students(request):
    students = Student.objects.all()
    return render(request, 'student.html', {'students' : students})

@login_required(login_url="login")
def enter_student(request):
    context = {}
    if request.method == "POST":
        form = StudentForms(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('student')
        else:
            context["form"] = form
    else:
        form = StudentForms()
        context["form"] = form
    return render(request, "add_student.html", context)
@login_required(login_url="login")
def delete_student(request, id):
    if request.method == "POST":
        student = get_object_or_404(Student, id=id)
        student.delete()
    return redirect('student')
@login_required(login_url="login")
def show_account_balance(request, id):
    student = get_object_or_404(Student, id=id)
    return render(request, 'account_balance.html', {
        'student': student
    })

@login_required(login_url="login")
def inventory_increase(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        inventory = int(request.POST.get("inventory"))
        inventory_user = int(student.account_balance) + inventory
        student.account_balance = str(inventory_user)
        student.save()

    return redirect('show_account_balance', id=student.id)

@login_required(login_url="login")
def inventory_reduction(request, id):
    student = get_object_or_404(Student, id=id) # یک شرط هست گرفتن شیء یا نمایش  404

    if request.method == "POST":
        inventory = int(request.POST.get("inventory"))
        inventory_user = int(student.account_balance) - inventory
        student.account_balance = str(inventory_user)
        student.save()

    return redirect('show_account_balance', id=student.id)
@login_required(login_url="login")
def show_list_food(request):
    food = DailyFood.objects.all()
    return render(request, 'food.html', {'food':food})
@login_required(login_url="login")
def enter_food(request):
    if request.method == "POST":
        form = DailyFoodForms(request.POST)
        if form.is_valid():
            form.save()
            return redirect("food")
    else:
        form = DailyFoodForms()
    return render(request, 'add_food.html')
@login_required(login_url="login")
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
@login_required(login_url="login")
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
