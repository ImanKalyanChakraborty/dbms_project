# DBMS Project

## Project Members

Iman Kalyan Chakraborty : Reg Number - 901
Anik Barury : Reg Number - 871

## Video Demo

## Instructions for Running it Locally

1. Clone This Repo

    `git clone https://github.com/ImanKalyanChakraborty/dbms_project.git`

2. Install dependencies

    `pip install -r requirements.txt`

3. Create the "railway_reservation_db" database in your MySQL Database

4. Change directory into "railway_reservation_system"

    `cd railway_reservation_system`

5. Run the following 3 commands to prepare the django backend

    `python manage.py makemigrations railway_reservation_system`
    `python manage.py migrate`
    `python manage.py runserver`

6. Open a new terminal window and write the following commands for starting up the frontend

    `cd railway_reservation_system`
    `python frontend.py`

7. Status of all of the tables can be viewed through the Django admin console
