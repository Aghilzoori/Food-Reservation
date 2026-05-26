from django import forms
from .models import Student, DailyFood

class StudentForms(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
                "full_name", 
                "national_code", 
                "account_balance",
                ]
class DailyFoodForms(forms.ModelForm):
    class Meta:
        model = DailyFood
        fields = [
            "day",
            "breakfast",
            "lunch",
            "dinner",
            "total_price",
        ]