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


from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from django.contrib.auth.models import Group


#The major backend logic for online guest house booking system

#Function to display the Homepage of the web system
def home(request):      
    return render(request=request, template_name="home.html")


#Function to Sign up new user
def sign_up(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.info(request, "Welcome to KGP")
            return redirect('index')
        else:
            messages.error(request, "Invalid Form Details")
    else:
        form = SignupForm()
    return render(request, 'user/sign-up.html', {'form': form})

#Function to Login in a new user
def login_request(request):                     #request variable takes a GET or POST HTTP request
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username= username, password=password)

            if user is not None:
                # Checking if a user if a staff
                if user.is_staff and not user.groups.filter(name='Staff').exists():
                    group = Group.objects.get(name='Staff')
                    user.groups.add(group) 
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('index')
            else:
                messages.error(request, "Invaild username or password")
        else:
            messages.error(request, "Invalid username or password.")        
    form = AuthenticationForm()
    return render(request, "user/login.html", context={"form":form})  


#Function to logout the user
def logout_request(request):                        #request variable takes a GET or POST HTTP request
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('home') 


#Function to change the password of the user
def change_password(request):                       #request variable takes a GET or POST HTTP request
    user = request.user
    if user.username and user.is_staff is False and user.is_superuser is False:
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():         #here user details are verified from database
                user = form.save()
                update_session_auth_hash(request.user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('change_password')
            else:
                messages.error(request, 'Please correct the error below:')
        else:
            form = PasswordChangeForm(request.user)
        return render(request, 'user/change_password.html', { 'form': form}) 
    else:
            messages.warning(request, 'You are not logged in. Please login') 
            return redirect('home')               

#Function to display the homepage of the user after login
def index(request):                                 #request variable takes a GET or POST HTTP request
        user = request.user
        if user.username and user.is_staff is False and user.is_superuser is False:
            if request.method == 'POST':
                form = ReservationForm(request.POST)
                if form.is_valid():
                    start_date = form.cleaned_data['start_date']
                    end_date = form.cleaned_data['end_date']
                    if start_date > end_date or start_date < datetime.date.today():
                        messages.warning(request, 'Please Enter Proper dates')
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
            messages.warning(request, 'You are not logged in. Please login') 
            return redirect('home')

#Function to Book the Rooms according to the parameters and show available rooms
def book(request, t):                               #request variable takes a GET or POST HTTP request
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
                    rooms_available = Rooms.objects.exclude(pk__in = R).filter(guesthouse_id=g.id)
                    no_rooms = 0
                    rooms = []

                    for t in rooms_available:
                        r = t.room_type
                        flag = 0
                        no_rooms = no_rooms+1  

                        for i in rooms:
                            if r in i.values():
                                i['count'] = i['count']+1
                                flag = 1
                              
                        if flag == 0:
                            rooms.append({'type': r, 'count': 1 })
                    context.append({ 'G': g, 'no_rooms': no_rooms, 'rooms': rooms})        
                return render(request, 'booking/available.html', {'rooms': context, 'T': tt })
        else:
            messages.warning(request, 'You are not logged in. Please login') 
            redirect('home') 
  

#Function to Query the rooms accoording to the given parameters and show results
def query(request):                                                 #request variable takes a GET or POST HTTP request
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
                    rooms_available = Rooms.objects.exclude(pk__in = R).filter(guesthouse_id=g.id)
                    no_rooms = 0
                    rooms = []

                    for t in rooms_available:
                        r = t.room_type
                        flag = 0

                        for i in rooms:
                            if r in i.values():
                                i['count'] = i['count']+1
                                flag = 1
                            no_rooms = no_rooms+1    
                        if flag == 0:
                            rooms.append({'type': r, 'count': 1 })
                    context.append({ 'G': g, 'no_rooms': no_rooms, 'rooms': rooms})

            return render(request, 'booking/available.html', {'rooms': context})
        else:
            messages.warning(request, 'Requested Page Not Found ')
            return redirect('home')
    else:
        form = ReservationForm(request.POST)
        return render(request, "booking/something.html", {'form' : form} )


#Function to Confirm booking and update the database
def book_room_verify(request, g, t, rtype, count):                              #request variable takes a GET or POST HTTP request
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
                R = Rooms.objects.filter(guesthouse=t.guesthouse).filter(room_type=rtype)

                #res = Reservation.objects.all()

                rooms = []
                for re in T:
                    rooms.append(re.rooms_allocated)

                for rd in R:
                    if rd not in rooms:
                        xyz = rd
                        break    

                newreservation = Reservation()  #here reservation is added  to database on confirmation
                newreservation.bookingID = str(xyz.roomID)+str(user.username)+str(datetime.date.today())    
                newreservation.start_date = start_date
                newreservation.end_date = end_date
                newreservation.user_booked = user
                newreservation.booktime = datetime.date.today()
                newreservation.guesthouse = t.guesthouse
                newreservation.status = True
                newreservation.room_type = rtype
                newreservation.rooms_allocated = xyz
                newreservation.save()


                newpayment = Payment()  #payment is generated on confirm reservation
                newpayment.paymentID = str(newreservation.bookingID)+str(xyz.price*(0.2)) 		
                newpayment.amount = (xyz.price * 0.2) 
                newpayment.reservation = newreservation
                newpayment.user_booked = user
                newpayment.payment_time = datetime.date.today()  
                newpayment.save()

                return render(request, "booking/book_successful.html", {'reservation' : newreservation}) 
                
            else:
                messages.warning(request, 'Requested Page Not Found ')
                #return redirect('home')
                return redirect('index')
        else:
            messages.warning(request, 'You are not logged in. Please login')
            return redirect('home')


#Function to cancel the reserved rooms
def cancel(request, id):                                    #request variable takes a GET or POST HTTP request
            user = request.user
            if user.username and user.is_staff is False and user.is_superuser is False:

                reservation = Reservation.objects.get(id = id)
                room_1 = reservation.rooms_allocated
                reservation.status = False
                reservation.save()
                flag = 0
            


                """ for waiting_one in WaitingOn.objects.all():
                    start_date = waiting_one.start_date 
                    end_date = waiting_one.end_date
                    res_3 = waiting_one.resID

                    T = Reservation.objects.filter(
                    Q(start_date__range=(start_date, end_date)) | Q(end_date__range=(start_date, end_date))).filter(status=True).filter(waiting=False)

                    for r in T:
                        if(r == reservation):
                            new_reservation = waiting_one.resID
                            new_reservation.waiting = False
                            new_reservation.rooms_allocated = reservation.rooms_allocated
                            new_reservation.save()
                            waiting_one.delete()
                            flag = 1
                            break

                    if flag == 1:
                        break  
                """


                for waiting_one in WaitingOn.objects.all():
                    start_date = waiting_one.start_date 
                    end_date = waiting_one.end_date
                    res_3 = waiting_one.resID

                    T = Reservation.objects.filter(
                    Q(start_date__range=(start_date, end_date)) | Q(end_date__range=(start_date, end_date))).filter(status=True).filter(waiting=False).filter(room_type = res_3.room_type).filter(guesthouse = res_3.guesthouse)

                        
                    R = Rooms.objects.filter(guesthouse=res_3.guesthouse).filter(room_type=res_3.room_type)

                    rooms = []
                    for re in T:
                        f = re.rooms_allocated
                        if f not in rooms:
                            rooms.append(f)

                    for room_of in R:
                        if room_of not in rooms:
                            xyz = room_of
                            flag = 1

                            res_3.rooms_allocated = xyz
                            res_3.waiting = False
                            res_3.save()
                            waiting_one.delete()
                            break



                    if flag == 1:
                        break            
    

                newrefund = Refund()        #on cancellation of confirmed reservation, refund is generated automatically
                newrefund.refundID = str(reservation.bookingID)+str(user.username)
                newrefund.reservation = reservation
                newrefund.amount = reservation.rooms_allocated.price*(0.2)
                newrefund.user_booked = user
                newrefund.refund_time = datetime.date.today()

                payments = reservation.payments.all()

                for p in payments:
                    res =p.reservation
                    if(res.id == id):
                        newrefund.payment = p
                
                newrefund.save()      

                messages.warning(request, 'Your Booking with Booking number  ' + str(reservation.bookingID) + ' is cancelled Succesfully')
                return render(request,"booking/cancel_successful.html", {'reservation' : reservation })
            else:
                messages.warning(request, 'you are not logged in or have no access')
                return redirect('login')

#Function to show all the Booking of the Logged in user 
def my_bookings(request):                                               #request variable takes a GET or POST HTTP request
        user = request.user
        if user.username and user.is_staff is False and user.is_superuser is False:
            T = Reservation.objects.filter(user_booked=user).order_by('-booktime').filter(status=True)
            bookings = []
            
            for t in T:
                g = t.guesthouse
                #d = GuestDetails.objects.filter(transaction=t.id)
                r = t.rooms_allocated
                bookings.append({'T': t , 'G': g, 'R':r})
            context = {'bookings': bookings, 'reservation': T}
            return render(request, 'booking/my_bookings.html', context)
        else:
            messages.warning(request, 'You are not authorized to acces the requested page. Please Login ')
            return redirect('home')
    
#Function to provide booking option for the Waiting queue
def waiting_show(request, t):                           #request variable takes a GET or POST HTTP request
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
                                Q(start_date__range =(start_date, end_date)) | Q(end_date__range =(start_date, end_date))).filter(status=True).filter(guesthouse=g)

                    rooms = []
                    for t in new_waiting:
                        R = t.room_type
                        flag = 0

                        for i in rooms:
                            if R in i.values():
                                i['count'] = i['count']+1
                                flag = 1
                            
                        if flag == 0:
                            rooms.append({'type': R, 'count': 1 })

             
                    context.append({'G' : g, 'room2' : rooms})    
      
                return render(request, 'booking/waiting_show.html', {'rooms': context, 'T': tt })
        else:
            messages.warning(request, 'You are not logged in. Please login') 
            redirect('home') 


#Function to put the logged in user into the queue
def waiting(request, g, t, rtype):                                      #request variable takes a GET or POST HTTP request
        user = request.user
        if user.username and user.is_staff is False and user.is_superuser is False:
            if request.method == 'POST':
                t = PreReservation.objects.get(id=t)
                t.guesthouse = GuestHouse.objects.get(id=g)
                t.save()

                
                
                newreservation = Reservation()      #here a waiting reservation is created
                newreservation.bookingID = str(t.guesthouse.code)+str(t.id)    
                newreservation.start_date = t.start_date
                newreservation.end_date = t.end_date
                newreservation.user_booked = user
                newreservation.room_type = rtype
                newreservation.booktime = datetime.date.today()
                newreservation.guesthouse = t.guesthouse
                newreservation.status = True
                newreservation.waiting = True
                newreservation.save()

                R = Rooms.objects.filter(guesthouse = t.guesthouse).filter(room_type = rtype)


                newpayment = Payment()  #payment is done on waiting reservation is confirmed
                newpayment.paymentID = str(newreservation.bookingID)+str(R[0].price*(0.2)) 		
                newpayment.amount = R[0].price * (0.2) 
                newpayment.reservation = newreservation
                newpayment.user_booked = user
                newpayment.payment_time = datetime.date.today()  
                newpayment.save()


                newwaiting = WaitingOn() #here reservation is added to waiting queue so that on cancellation of any reservation, it gets confirmwed automatically
                newwaiting.resID = newreservation
                newwaiting.date_booked = newreservation.booktime
                newwaiting.start_date = newreservation.start_date
                newwaiting.end_date = newreservation.end_date
                newwaiting.save()

                return render(request, "booking/waiting_successful.html", {'reservation' : newreservation, 'waiting': newwaiting, 'payment':newpayment }) 
                
            else:
                messages.warning(request, 'Requested Page Not Found ')
                return redirect('index')
        else:
            messages.warning(request, 'You are not logged in. Please login')
            return redirect('home')


#Function to provide form to the user to fill in the feedback
def feedback(request):                                      #request variable takes a GET or POST HTTP request
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
    
        form = FeedbackForm()
        return render(request, "booking/feedback.html", context={"form":form})                
    
    else:
        messages.warning(request, 'You are not logged in. Please login') 
        redirect('home') 

#Function to cancel the waitlisted reservations
def cancelwaiting(request, id):                                             #request variable takes a GET or POST HTTP request
            user = request.user
            if user.username and user.is_staff is False and user.is_superuser is False:

                reservation = Reservation.objects.get(id = id)
                reservation.status = False
                reservation.save()
                
            
    

                newrefund = Refund()            # here refund is done automatically on cancellation of reservation
                newrefund.refundID = str(reservation.bookingID)+str(user.username)
                newrefund.reservation = reservation
                newrefund.user_booked = user
                newrefund.refund_time = datetime.date.today()

                payments = reservation.payments.all()

                for p in payments:
                    res = p.reservation
                    if(res.id == id):
                        newrefund.payment = p
                        newrefund.amount = p.amount
                
                newrefund.save()      

                messages.warning(request, 'Your Booking with Booking number  ' + str(reservation.bookingID) + ' is cancelled Succesfully')
                return render(request,"booking/cancel_successful.html", {'reservation' : reservation })

            else:
                messages.warning(request, 'you are not logged in or have no access')
                return redirect('login')
   
#Function to provide room details
def roomdetails(request):                                           #request variable takes a GET or POST HTTP request
        user = request.user
        if user.username and user.is_staff is False and user.is_superuser is False:
            if request == 'POST':
                return render(request, "booking/roomdetails.html")
            else:
                messages.warning(request, 'something went wrong')
                return redirect('index')
        else:  
            messages.warning(request, 'you are not logged in or have no access')
            return redirect('login')          




