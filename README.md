# nest4guest
This is a Python based online guest house booking portal. The app is a one time solution that makes it easier for users to query and book rooms, review status of booking (incase all rooms are booked, user can add their rooms in waitlist) and cancel booking. It also includes automatic confirmation of next booking from waiting list on cancellation of a booking.

## Prerequisite/libraries used
  1. **Python3(3.6 +)**
  2. **Django(2.1 +)** to install django, open terminal and type pip3 install Django.    

This code was written using Python3 and Django2.

## Usage
  1. Install django2 and other dependencies(as stated in requirements.txt). 
  2. Clone the repo to your local machine.
  3. To start the server go to the repo directory in terminal and type python3 manage.py runserver. Note:Keep this running as long as you are using the website.
  4. Now open browser and visit 127.0.0.1:8000/home(or something similar that appeared on terminal when previous command was run).       This is the home-page of this web-site.(locally).
    Navigate like a normal web-site.

  5. If you want to see or edit the database/user info, you can add your own super-user by running python3 manage.py createsuperuser in the repo's directory. After creating superuser, use the credentials on 127.0.0.1:8000/admin/(or whatever your machine's local host is) to log-in and view the database.

## Test Version

  One can see the demo version of app deployed on heroku. 
  For that just visit the following url : https://nest4guest.herokuapp.com/home/
