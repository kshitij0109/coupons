from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Coupon, Claim
from django.utils.timezone import now
from datetime import timedelta

def get_client_ip(request):
    """Get user's IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')

def claim_coupon(request):
    ip = get_client_ip(request)
    session_id = request.session.session_key or request.session.create()

    # Check cooldown (prevent multiple claims within 10 minutes)
    recent_claims = Claim.objects.filter(ip_address=ip, claimed_at__gte=now() - timedelta(minutes=10))
    if recent_claims.exists():
        return JsonResponse({"message": "You can only claim one coupon every 10 minutes!"}, status=403)

    # Get the next available coupon
    coupon = Coupon.objects.filter(is_active=True).first()
    if not coupon:
        return JsonResponse({"message": "No coupons available."}, status=404)

    # Assign the coupon and log the claim
    Claim.objects.create(coupon=coupon, ip_address=ip, session_id=session_id)
    coupon.is_active = False
    coupon.save()

    return JsonResponse({"message": f"Coupon '{coupon.code}' claimed successfully!"})

def home(request):
    """Render the homepage"""
    return render(request, "index.html")
