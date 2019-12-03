f# nest4guest
This is a python based online guest house booking portal. The app is a one time solution that makes it easier for users to query and book rooms, review status and cancel booking.  Included automatic confirmation of next booking from waiting list on cancellation of a booking
## Prerequisite/libraries used
  1. **Python3(3.6 +)**
  2. **Django(2.1 +)** to install django, open terminal and type pip3 install Django.    

This code was written using Python 3.6.7 and Django 2.1.7.

## Usage(on ubuntu 16 and above)
  1. Clone or Fetch this repo to your local machine.
  2. To start the server go to the repo directory in terminal and type python3 manage.py runserver. Note:Keep this running as long as you are using the website.
  3. Now open browser and visit 127.0.0.1:8000/(or something similar that appeared on terminal when previous command was run).       This is the home-page of this web-site.(locally).
    Navigate like a normal web-site.

  4. If you want to see or edit the database/user info, you can add your own super-user by running python3 manage.py createsuperuser in the repo's directory. After creating superuser, use the credentials on 127.0.0.1/8000:admin/(or whatever your machine's local host is) to log-in and view the database.

## Test Version

  One can see the demo version of app deployed on heroku. For that just visit the following url   https://nest4guest.herokuapp.com/home/
