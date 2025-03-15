from django.db import models

class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

class Claim(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    session_id = models.CharField(max_length=255)
    claimed_at = models.DateTimeField(auto_now_add=True)
