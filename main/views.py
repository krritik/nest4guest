from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.models import Q

from django.db.models import Count
from . forms import *
from . models import * 
import datetime


def home(request):
    return render(request=request, template_name="home.html")

def sign_up(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignupForm()
    return render(request, 'user/sign-up.html', {'form': form})

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username= username, password=password)

            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('index')
            else:
                messages.error(request, "Invaild username or password")
        else:
            messages.error(request, "Invalid username or password.")        
    form = AuthenticationForm()
    return render(request, "user/login.html", context={"form":form})  

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('home')  

def index(request):
        user = request.user
        if user.username and user.is_staff is False and user.is_superuser is False:
            if request.method == 'POST':
                form = ReservationForm(request.POST)
                if form.is_valid():
                    start_date = form.cleaned_data['start_date']
                    end_date = form.cleaned_data['end_date']
                    if start_date > end_date or start_date < datetime.date.today():
                        messages.warning(request, 'Pelase Enter Proper dates')
                        return redirect('index')
                    T = PreReservation()
                    T.start_date = start_date
                    T.end_date = end_date
                    T.save()
                    return redirect('book', T.id)
                else:
                    for e in form.errors:
                        messages.error(request, e)
                    return redirect('index')
            else:
                form = ReservationForm(request.POST)
                return render(request, "user/index.html", {'form' : form} )        
        else:
            return redirect('home')


def book(request, t):
        user =request.user
        if user.username and user.is_staff is False and user.is_superuser is False:
            if request.method == 'POST':
                return redirect('index')
            else:
                tt = PreReservation.objects.get(id = t)
                start_date = tt.start_date
                end_date = tt.end_date
            
                T = Reservation.objects.filter(
                    Q(start_date__range =(start_date, end_date)) | Q(end_date__range =(start_date, end_date))).filter(status = True).filter(waiting=False)
                   
                R = []
                for t in T:
                    f = t.rooms_allocated    
                    if f.id not in R:
                            R.append(f.id)
                    
                G = GuestHouse.objects.all()
                context = []
                for g in G:
                    rooms_available = Rooms.objects.exclude(pk__in = R).filter(guesthouse_id=g.id).values(
                        'room_type').annotate(count=Count('room_type'))
                    no_rooms = 0
                    rooms = []
                    for room in rooms_available:
                        types  = str(room.get('room_type'))
                        count = room.get('count')
                        rooms.append({'type': types, 'count': count})      
                        no_rooms = no_rooms + count
                    context.append({ 'G': g, 'no_rooms': no_rooms, 'rooms': rooms})
      
                return render(request, 'booking/available.html', {'rooms': context, 'T': tt })
        else:
            messages.warning(request, 'Page Not Found') 
            redirect('home') 
  


def query(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            if start_date > end_date or start_date < datetime.date.today():
                messages.warning(request, 'Please Enter Proper dates')
                return redirect('home')
            T = Reservation.objects.filter(
                Q(start_date__range=(start_date, end_date)) | Q(end_date__range=(start_date, end_date)))
            R = []
            for t in T:
                f = t.rooms_allocated
                for g in f:
                    if g.id not in R:
                        R.append(g.id)
            G = GuestHouse.objects.all()
            context = []
            for g in G:
                rooms_available = Rooms.objects.exclude(pk__in=R).filter(guesthouse_id=g.id).values(
                    'room_type').annotate(count=Count('room_type'))
                no_rooms = 0
                rooms = []
                for room in rooms_available:
                    types = str(room.get('room_type'))
                    count = room.get('count')
                    rooms = {'type': types, 'count': count }
                    no_rooms = no_rooms + count
                context = {'G': g, 'no_rooms': no_rooms, 'rooms': rooms} 
            return render(request, 'booking/availability.html', {'rooms': context})
        else:
            messages.warning(request, 'Requested Page Not Found ')
            return redirect('home')
    else:
        form = ReservationForm(request.POST)
        return render(request, "booking/something.html", {'form' : form} )


def book_room_verify(request, g, t, rtype, count):
    #try:
        user = request.user
        if user.username and user.is_staff is False and user.is_superuser is False:
            if request.method == 'POST':
                t = PreReservation.objects.get(id=t)
                t.guesthouse = GuestHouse.objects.get(id=g)
                t.save()

                start_date = t.start_date
                end_date = t.end_date

                T = Reservation.objects.filter(
                    Q(start_date__range=(start_date, end_date)) | Q(end_date__range=(start_date, end_date))).filter(status=True).filter(waiting=False)

                R = []
   
                for d in T:
                    f = d.rooms_allocated
                    if f.id not in R:
                            R.append(f.id)
                R = Rooms.objects.filter(guesthouse=t.guesthouse).filter(room_type=rtype)[0]


                newreservation = Reservation()
                newreservation.bookingID = str(R.roomID)+str(user.username)+str(datetime.date.today())    
                newreservation.start_date = start_date
                newreservation.end_date = end_date
                newreservation.user_booked = user
                newreservation.booktime = datetime.date.today()
                newreservation.guesthouse = t.guesthouse
                newreservation.status = True
                newreservation.room_type = rtype
                newreservation.rooms_allocated = R
                newreservation.save()


                newpayment = Payment()
                newpayment.paymentID = str(newreservation.bookingID)+str(R.price) 		
                newpayment.amount = R.price
                newpayment.reservation = newreservation
                newpayment.user_booked = user
                newpayment.payment_time = datetime.time.today()  
                newpayment.save()

                return render(request, "booking/book_successful.html", {'reservation' : newreservation}) 
                
            else:
                messages.warning(request, 'Requested Page Not Found ')
                #return redirect('home')
                return redirect('index')
        else:
            messages.warning(request, 'Requested Page Not Found ')
            return redirect('home')
   # except Exception as e:
    #    messages.warning(request, 'Something Went Wrong. Please Try agin')
     #   return redirect('index')



def cancel(request, id):
    try:
        if request.method == 'POST':
            return redirect('my_bookings')
        else:
            user = request.user
            if user.username and user.is_staff is False and user.is_superuser is False:

                reservation = Reservation.objects.get(id = id)
                
                for waiting_one in WaitingOn:
                    start_date = waiting_one.start_date 
                    end_date = waiting_one.end_date

                    T = Reservation.objects.filter(
                    Q(start_date__range=(start_date, end_date)) | Q(end_date__range=(start_date, end_date))).filter(status=True).filter(waiting=False)

                    if(len(T) > 1):
                        continue
                    elif(len(T) == 1):
                        if(T == reservation):
                            new_reservtaion = waiting_one.resID
                            new_reservation.waiting = False
                            new_reservtaion.save()
                            waiting_one.delete()
                            break
                    else:       
                        continue

                
                reservation.status = False
                reservation.save()

                newrefund = Refund()
                newrefund.refundID = str(newreservation.bookingID)+str(R.roomID)
                newrefund.reservation = reservation
                newrefund.amount = reservation.room_allocated.price
                newrefund.user = user
                newrefund.refund_time = datetime.date.today()

                payments = reservation.payments.objects.all()
                newrefund.payment = payments.filter(reservation = reservation.id)
                
                newrefund.save()
            
    

                    
                

                messages.warning(request, 'Your Booking with Booking number  ' + str(reservation.bookingID) + ' is cancelled Succesfully')
                return redirect('my_bookings')
            else:
                messages.warning(request, 'you are not logged in or have no access')
                return redirect('login')
    except Exception as e:
        messages.warning(request, str(e))
        return redirect('home')     

def my_bookings(request):
   # try:
        user = request.user
        if user.username and user.is_staff is False and user.is_superuser is False:
            T = Reservation.objects.filter(user_booked=user).order_by('-booktime').filter(status=True)
            bookings = []
            
            for t in T:
                g = t.guesthouse
                #d = GuestDetails.objects.filter(transaction=t.id)
                r = t.rooms_allocated
                bookings.append({'T': t , 'G': g, 'R':r})
            context = {'bookings': bookings, 't': T}
            return render(request, 'booking/my_bookings.html', context)
        else:
            messages.warning(request, 'You are not authorized to acces the requested page. Please Login ')
            return redirect('home')
    #except Exception as e:
    #    messages.warning(request, str(e))
#return redirect('error')


def waiting_show(request, t):
        user =request.user
        if user.username and user.is_staff is False and user.is_superuser is False:
            if request.method == 'POST':
                return redirect('index')
            else:
                tt = PreReservation.objects.get(id = t)
                start_date = tt.start_date
                end_date = tt.end_date
            
                G = GuestHouse.objects.all()
                context = []

                for g in G:
                    new_waiting = Reservation.objects.filter(
                                Q(start_date__range =(start_date, end_date)) | Q(end_date__range =(start_date, end_date))).filter(waiting=True).filter(status=True).filter(guesthouse=g)

                    rooms = []
                    for t in new_waiting:
                        R = t.room_type
                        flag = 0

                        for i in rooms:
                            if R in i.values():
                                i['count'] = i['count']+1
                                flag = 1
                            
                        if flag == 0:
                            rooms.append({'type': R,' count': 0 })

                    room_left = Rooms.objects.filter(guesthouse = g)

                    for room_3 in room_left:
                        R = room_3.room_type
                        flag = 0
                        for i in rooms:
                            if R in i.values():
                                flag = 1

                        if flag == 0:       
                            rooms.append({'type': room_3.room_type, 'count': 0})

                    context.append({'G' : g, 'room2' : rooms})    
      
                return render(request, 'booking/waiting_show.html', {'rooms': context, 'T': tt })
        else:
            messages.warning(request, 'Page Not Found') 
            redirect('home') 


def waiting(request, g, t, rtype):
        user = request.user
        if user.username and user.is_staff is False and user.is_superuser is False:
            if request.method == 'POST':
                t = PreReservation.objects.get(id=t)
                t.guesthouse = GuestHouse.objects.get(id=g)
                t.save()

                
                
                newreservation = Reservation()
                newreservation.bookingID = str(t.guesthouse.code)+str(t.id)    
                newreservation.start_date = t.start_date
                newreservation.end_date = t.end_date
                newreservation.user_booked = user
                newreservation.booktime = datetime.date.today()
                newreservation.guesthouse = t.guesthouse
                newreservation.status = True
                newreservation.waiting = True
                newreservation.save()


                newwaiting = WaitingOn()
                newwaiting.resID = newreservation
                newwaiting.date_booked = newreservation.booktime
                newwaiting.start_date = newreservation.start_date
                newwaiting.end_date = newreservation.end_date
                newwaiting.save()

                return render(request, "booking/waiting_successful.html", {'reservation' : newreservation, 'waiting': newwaiting }) 
                
            else:
                messages.warning(request, 'Requested Page Not Found ')
                #return redirect('home')
                return redirect('index')
        else:
            messages.warning(request, 'Requested Page Not Found ')
            return redirect('home')

def feedback(request):
    user = request.user
    if user.username and user.is_staff is False and user.is_superuser is False:
        if request.method == 'POST':   
            form = FeedbackForm(request.POST)
            if form.is_valid():
                feed = form.cleaned_data.get('feed')

                newfeedback = Feedback()
                newfeedback.user_of = user
                newfeedback.time = datetime.date.today()
                newfeedback.feed = feed
                newfeedback.feedbackID = str(user.username)+str(datetime.date.today())+str(user.email)
                newfeedback.save()

                return render(request, "booking/feedback_successful.html")
            else:
                messages.error(request, "Invalid form details")
        else:                
            form = FeedbackForm()
            return render(request, "booking/feedback.html", context={"form":form})                
    else:
        messages.warning(request, 'Page Not Found') 
        redirect('home') 
   