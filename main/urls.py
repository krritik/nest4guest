from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('signup/', views.sign_up, name='signup'),
    path('logout/', views.logout_request, name='logout'),
    path('login/', views.login_request, name='login'),
    path('profile/', views.index, name='index'),
    path('password/', views.change_password, name='change_passsword'),

    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('query/', views.query, name='query'),
    path('book/<int:t>', views.book, name='book'),
    path('book/<int:g>/<int:t>/<slug:rtype>/<int:count>/', views.book_room_verify, name='book_room_verify'),
    path('cancel/<int:id>/', views.cancel, name='cancel'),
    path('cancel_waiting/<int:id>/', views.cancelwaiting, name = 'cancelwaiting'),
    
    path('waiting/<int:t>/', views.waiting_show, name='waiting_show'),
    path('waiting/<int:g>/<int:t>/<slug:rtype>/', views.waiting, name='waiting'),
    path('feedback/', views.feedback, name='feedback'),

    path('password_change/', auth_views.PasswordChangeView.as_view(), {'template_name': 'user/change_password.html'},name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(),name='password_change_done'),


    path('roomdetails/', views.roomdetails, name = 'roomdetails'),
]