from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class GuestHouse(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
    code = models.CharField(max_length=3, null=True, unique=True)

    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name  

class Rooms(models.Model):
    roomID = models.CharField( default=None, max_length=30)
    ROOM_TYPES = [
        ('Single-AC', 'Single-AC'),
        ('Double-AC', 'Double-AC'),
        ('Single-NON-AC', 'Single NON-AC'),
        ('Double-NON-AC', 'Double-NON-AC'),
    ]
    room_type = models.CharField( max_length=20, choices=ROOM_TYPES, null=False)
    guesthouse = models.ForeignKey(GuestHouse, on_delete=models.CASCADE, null=False, blank=False)
    price = models.PositiveIntegerField( default=None, blank=False, null=False)
    services = models.CharField( default="No special services available", null=True, max_length=50)
            
    class Meta:
        verbose_name_plural='Rooms'
        db_table = 'OGHBS_Rooms'
        ordering = ['roomID']
    
    def __str__(self):
        return self.roomID

class Reservation(models.Model):
    bookingID = models.CharField( default=None, max_length=30)
    start_date = models.DateTimeField(default=None, null=True)
    end_date = models.DateTimeField(default=None, null=True)
    
    user_booked = models.ForeignKey( User,on_delete=models.DO_NOTHING, null=False, blank=False)			
    #no_rooms = models.IntegerField(    null=True, blank=True)
    rooms_allocated = models.ForeignKey(Rooms, on_delete=models.CASCADE, null=True, blank=True)
    guesthouse = models.ForeignKey(GuestHouse, on_delete=models.CASCADE, null=True, blank=True)
    status = models.BooleanField(default=False)
    waiting = models.BooleanField(default=False)
    
    ROOM_TYPES = [
        ('Single-AC', 'Single-AC'),
        ('Double-AC', 'Double-AC'),
        ('Single-NON-AC', 'Single NON-AC'),
        ('Double-NON-AC', 'Double-NON-AC'),
    ]
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES, null=True, blank=True)
    booktime = models.DateField(null=False)
                
    class Meta:
        verbose_name_plural='Reservation'
        db_table = 'OGHBS_Reservation'
        ordering = ['-booktime']
                
    def __str__(self):
        return self.bookingID

class PreReservation(models.Model):
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)  
    #no_rooms = models.IntegerField(null=True, blank=True)
    guesthouse = models.ForeignKey(GuestHouse, on_delete=models.CASCADE, null=True, blank=True)
    ROOM_TYPES = [
        ('Single-AC', 'Single-AC'),
        ('Double-AC', 'Double-AC'),
        ('Single-NON-AC', 'Single NON-AC'),
        ('Double-NON-AC', 'Double-NON-AC'),
    ]
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES, null=True, blank=True)          

    def __str__(self):
        return  str(self.guesthouse) + ' || ' + str(self.start_date) + ' - ' + str(self.end_date)

class Payment(models.Model):
    paymentID = models.CharField( default=None, max_length=30)			
    amount = models.PositiveIntegerField( default=None, blank=False, null=False)
    reservation = models.ForeignKey('Reservation', on_delete=models.CASCADE, related_name='payments')
    user_booked = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    payment_time = models.DateField( default=timezone.now, null=False)
                
    class Meta:
        db_table = 'OGHBS_Payments'
        ordering = ['-payment_time']
                
    def __str__(self):
        return self.paymentID

class Refund(models.Model):

    refundID = models.CharField( default=None, max_length=30)
    payment = models.ForeignKey( 'Payment', on_delete=models.CASCADE)
    reservation = models.ForeignKey( 'Reservation', on_delete=models.CASCADE, related_name='refunds')
    amount = models.PositiveIntegerField( default=None, blank=False, null=False)
    user_booked = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    refund_time = models.DateTimeField( null=False)
                
    class Meta:
        db_table = 'OGHBS_Refunds'
        ordering = ['-refund_time']
                
    def __str__(self):
        return self.refundID        

class GuestDetails(models.Model):
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural='GuestDetails'

    def __str__(self):
        return self.first_name



class Feedback(models.Model):
    feedbackID = models.CharField( default=None, max_length=100)
    user_of = models.ForeignKey( User,on_delete=models.DO_NOTHING, null=False, blank=False)			
    time = models.DateField( default=timezone.now, null=False)
    feed = models.TextField( default=None)
                
    class Meta:
        db_table = 'OGHBS_feedbacks'
        ordering = ['-time']

    def __str__(self):
        return self.feedbackID


class WaitingOn(models.Model):
    resID = models.ForeignKey('Reservation', on_delete=models.CASCADE, null=False, blank=False)
    date_booked = models.DateField(default=timezone.now, null=False)     
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)  

    class Meta:
        verbose_name_plural='WaitingOn'
    
    
#class Message(models.Model):
#	messageID = models.CharField(null=True)
#	staff = models.ForeignKey(User, on_delete=models.CASCADE)
#    message = models.TextField( default=None)
#    time = models.DateTimeField(default=timezone.now, null=True)