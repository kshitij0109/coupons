from django.contrib import admin
from .models import Coupon, Claim

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ("code", "is_active")

@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ("coupon", "ip_address", "claimed_at")
