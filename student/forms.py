from django import forms
from .models import FoodReservation
class StudentLoginForm(forms.Form):
    full_name = forms.CharField(
        max_length = 200,
        label = "نام و نام خانوادگی",
        widget = forms.TextInput(attrs={"placeholder" : "مصطفی باقری زاده"})
    )
    national_code = forms.CharField(
        max_length = 10,
        label = "کد ملی",
        widget=forms.PasswordInput(attrs={'placeholder':'0721339669',})
    )