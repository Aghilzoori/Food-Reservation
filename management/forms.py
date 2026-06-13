from django import forms
from .models import Student, DailyFood

class StudentForms(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "full_name", 
            "national_code", 
            "account_balance",
            "profile",
        ]
        widgets = {  
            "full_name": forms.TextInput(attrs={"placeholder": "مصطفی باقری زاده"}), 
            "national_code": forms.TextInput(attrs={'placeholder': '0721339669'}), 
            "account_balance": forms.NumberInput(attrs={'placeholder': '5000000'}),
            "profile": forms.ClearableFileInput(),
        }
    def clean_national_code(self):
            national_code = self.cleaned_data.get("national_code")
            if national_code and str(national_code).isdigit():
                if len(national_code) == 10:
                    return national_code
                else:
                    raise forms.ValidationError("کد ملی شامل 10 رقم میباشد")
            else:
                raise forms.ValidationError("کد ملی شامل اعداد میباشد")
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