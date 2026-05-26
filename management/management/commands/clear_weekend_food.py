from django.core.management.base import BaseCommand
from django.utils import timezone
from management.models import DailyFood

class Command(BaseCommand):
    help = "حذف برنامه غذایی در آخر هفته"

    def handle(self, *args, **kwargs):
        today = timezone.now().strftime("%a").lower()

        # اگر جمعه بود
        if today == "fri":
            DailyFood.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("برنامه غذایی آخر هفته حذف شد ✅"))
        else:
            self.stdout.write("امروز آخر هفته نیست ❌")
