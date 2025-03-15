from django.urls import path , include
from . import views
urlpatterns = [
  
    path('', views.home, name='home'),
    path('claim/', views.claim_coupon, name="claim_coupon"),
]