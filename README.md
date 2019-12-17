# nest4guest
This is a Python based online guest house booking portal. The app is a one time solution that makes it easier for users to query and book rooms, review status of booking (incase all rooms are booked, user can add their rooms in waitlist) and cancel booking. It also includes automatic confirmation of next booking from waiting list on cancellation of a booking.

## Prerequisite/libraries used:
  1. **Python3(3.6 +)**
  2. **Django(2.1 +)** to install django, open terminal and type pip3 install Django.    

This code was written using Python3 and Django2.

## Usage:
  1. Clone the repo to your local machine.
  2. Install django2 and other dependencies(as stated in requirements.txt). 
  3. To start the server go to the repo directory in terminal and type python3 manage.py runserver. Note:Keep this running as long as you are using the website.
  4. Now open browser and visit 127.0.0.1:8000(or something similar that appeared on terminal when previous command was run).       This is the home-page of this web-site.(locally).
    Navigate like a normal web-site.

  5. If you want to see or edit the database/user info, you can add your own super-user by running python3 manage.py createsuperuser in the repo's directory. After creating superuser, use the credentials on 127.0.0.1:8000/admin/(or whatever your machine's local host is) to log-in and view the database.


## Test Version

  One can see the demo version of app deployed on heroku. 
  For that just visit the following url : https://nest4guest.herokuapp.com/

## Contribution Guidelines:

  1. Do a self-review of your code and comment important sections.
  2. One must deploy locally to see if issue is fixed.
  3. One can take an issue, assigning is not important (so others can also work on that)
  4. If somebody has a WIP( work in progress ), then issue can be assigned so that somebody does not send another pr for same issue. But you should write in comments of the issue that you would like to take it with the proposed solution.
