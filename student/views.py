from django.shortcuts import render, redirect, get_object_or_404
from management.models import Student, DailyFood
from .forms import StudentLoginForm
from .models import FoodReservation
from django.utils import timezone

WEEK_ORDER_IRAN = ["sat", "sun", "mon", "tue", "wed", "thu", "fri"]

def get_iran_day_index(day_code):

    return WEEK_ORDER_IRAN.index(day_code)

def get_today_iran_index():
    py_day = timezone.now().weekday()
    return (py_day + 2) % 7

def student_login(request):
    error = None
    if request.method == "POST":
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data["full_name"]
            national_code = form.cleaned_data["national_code"]
            try:
                student = Student.objects.get(
                    full_name=full_name,
                    national_code=national_code
                )
                request.session["student_id"] = str(student.id)
                return redirect("student_dashboard")
            except Student.DoesNotExist:
                error = "اطلاعات وارد شده صحیح نیست"
    else:
        form = StudentLoginForm()
    return render(request, "student_login.html", {
        "form": form,
        "error": error
    })

def student_dashboard(request):
    student_id = request.session.get("student_id")
    if not student_id:
        return redirect("student_login")
    student = Student.objects.get(id=student_id)
    dailyfood = DailyFood.objects.all()
    my_reservations = FoodReservation.objects.filter(student=student)
    
    return render(request, "student_dashboard.html", {
        "student": student,
        "dailyfood": dailyfood,
        "my_reservations": my_reservations
    })

def student_logout(request):
    request.session.flush()
    return redirect("student_login")

def wallet_help(request):
    return render(request, "help.html")

def food_reservation(request, reservation_id): 
    student_id = request.session.get("student_id")
    if not student_id:
        return redirect("student_login")
    
    student = Student.objects.get(id=student_id)
    food = get_object_or_404(DailyFood, id=reservation_id) 
    
    today_index = get_today_iran_index()
    food_day_index = get_iran_day_index(food.day)
    
    if today_index == food_day_index:
        return render(request, "reservation_error.html", {
            "error": "❌ تاریخ این غذا گذشته است"
        })
    
    if FoodReservation.objects.filter(student=student, food=food).exists():
        return render(request, "reservation_error.html", {
            "error": "⚠️ شما قبلاً این غذا را رزرو کرده‌اید"
        })
    
    price = food.total_price if food.total_price is not None else 0
    
    if student.account_balance < price:
        return render(request, "reservation_error.html", {
            "error": f"❌ موجودی حساب کافی نیست! (مبلغ مورد نیاز: {price} تومان)"
        })
    
    student.account_balance -= price
    student.save()
    
    FoodReservation.objects.create(
        student=student,
        food=food
    )
    
    return redirect("student_dashboard")

def delete_reservation(request, reservation_id):
    student_id = request.session.get("student_id")
    if not student_id:
        return redirect("student_login")
    
    reservation = get_object_or_404(FoodReservation, id=reservation_id, student_id=student_id)
    
    food_day_index = get_iran_day_index(reservation.food.day)
    today_index = get_today_iran_index()
    
    if food_day_index == today_index:
        return render(request, "reservation_error.html", {"error": "⏰ مهلت لغو این رزرو تمام شده است (غذا مربوط به امروز است)"})
    else:
        price = reservation.food.total_price if reservation.food.total_price is not None else 0
        
        reservation.student.account_balance += price
        reservation.student.save()
        
        reservation.delete()
        
        return redirect('student_dashboard')