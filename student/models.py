from django.db import models
from management.models import Student, DailyFood
import uuid
class FoodReservation(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="reservations"
    )

    food = models.ForeignKey(
        DailyFood,
        on_delete=models.CASCADE,
        related_name="reservations"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.food}"

    

# Create your models here.
