from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Stock(models.Model):
    ticker = models.CharField(max_length=10)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default="")
    bottom = models.FloatField(default=0.00)
    top = models.FloatField(default=1000.00)
    period = models.IntegerField(default=60)

    def __str__(self):
        return str(self.ticker)

    def get_data(self):
        ans = {
            "top": self.top,
            "bottom": self.bottom,
            "period": self.period,
        }
        return ans

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["ticker", "owner"], name="unicidade")
        ]
