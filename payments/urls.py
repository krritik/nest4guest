from django.urls import path 
from . import views

urlpatterns = [
    path('payment/<int:g>/<int:t>/<slug:rtype>/<int:count>/', views.PaymentPageView.as_view(), name='payment'),
]
