from django.db import models
import uuid
class Student(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    full_name = models.CharField(
        max_length=200,
        verbose_name="نام و نام خانوادگی"
    )

    national_code = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="کد ملی"
    )

    account_balance = models.IntegerField(
        verbose_name="موجودی حساب"
    )
    
    profile = models.ImageField(
        null=True, 
        blank=True, 
        default='default.jpg', 
        verbose_name="پروفایل"
        )

    def __str__(self):
        return self.full_name
    
class DailyFood(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    DAY_CHOICES = [
        ('sat', 'شنبه'),
        ('sun', 'یک شنبه'),
        ('mon', 'دوشنبه'),    # ایندکس 0 مقداری است که در دیتابیس ذخیره می‌شود، ایندکس 1 مقداری است که به کاربر نمایش داده می‌شود
        ('tue', 'سه شنبه'),   # قوانین Django: مقادیر choices یک لیست از tuple هستند. مقدار اول ذخیره و مقدار دوم نمایش داده می‌شود
        ('wed', 'چهارشنبه'),
        ('thu', 'پنج شنبه'),
        ('fri', 'جمع'),
    ]

    # مرجع: https://docs.djangoproject.com/en/4.2/ref/models/fields/#choices


    day = models.CharField(max_length=3, choices=DAY_CHOICES, unique=True)

    breakfast = models.CharField(
        max_length=200, blank=True, null=True, verbose_name='صبحانه'
    )
    lunch = models.CharField(
        max_length=200, blank=True, null=True, verbose_name='ناهار'
    )
    dinner = models.CharField(
        max_length=200, blank=True, null=True, verbose_name='شام'
    )

    total_price = models.IntegerField(
        blank=True, null=True, verbose_name='قیمت کل روز'
    )

    def __str__(self):
        return dict(self.DAY_CHOICES).get(self.day, self.day)
