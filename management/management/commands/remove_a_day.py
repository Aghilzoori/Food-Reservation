from django.core.management.base import BaseCommand
from django.utils import timezone
from management.models import DailyFood

class Command(BaseCommand):
    help = "حذف یک روز از داده ها"

    def handle(self, *args, **kwargs): 
        today = timezone.localtime(timezone.now()).strftime("%A").lower()
        try:
            obj = DailyFood.objects.get(day=str(today[:3]))
            obj.delete()
        except DailyFood.DoesNotExist:
            print("No object for today")
        except DailyFood.MultipleObjectsReturned:
            objs = DailyFood.objects.filter(day=today)
            objs.delete()