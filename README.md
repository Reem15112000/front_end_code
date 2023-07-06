Hospital graduation project

in order to run the project you need to run the following commands:
- make sure you have python3 installed
- run `python3 -m venv venv`
- run `source venv/bin/activate` on linux or `venv\Scripts\activate` on windows
- run `pip install -r requirements.txt`
- copy the `.env.example` file to `.env` and fill the required fields (for local developmennt you can leave the default values)
- run `python manage.py migrate`
- run `python manage.py runserver`

now you can reach the server using 'http://127.0.0.1:8000'.

## API Documentation
these are all the available endpoints that you can use. 

/api/hospitals/
/api/sections/
/api/doctors/
/api/register/
/api/login/
/api/doctor-details/
/api/my-reservations/
/api/my-consulations/
/api/my-consulations/<int:pk>/

## Create a new superuser
- run `python manage.py createsuperuser`
after entering the credentials you will be able to access the admin page using 
'http://127.0.0.1:8000/admin/'.
