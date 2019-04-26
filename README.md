# Goshna Server

## 1 Prerequisites

Requires Python 2.7.

Download and install:
> sudo apt-get install python-2.7 python-pip

Or alternatively, from: https://www.python.org/downloads/

Ensure Python is added to your PATH environment variable. There is an option to do this during the installation on Windows, or you can follow the instructions here:
https://docs.python.org/3/using/windows.html#excursus-setting-environment-variables

Note: Migration to Python 3 will occur in a future update.

## 2 Install

> ./install.sh

### 2.2 Install (Windows)

Install the Python Virtual Environment package:
> pip install virtualenv

Navigate to the Goshna Server folder and create a Virtual Environment:
> python "C:\Python27\Scripts\virtualenv.exe" .venv

Activate the Virtual Environment for Goshna:
> .venv\Scripts\activate.bat

Install the projects Python dependencies:
> pip install -r requirements.txt

## 3 Run (debug/testing)

1) Activate the VirtualEnvironment (if not already active):

> source .venv/bin/activate

2a) then run the application directly:

> PYTHONPATH=.. python app.py

2b) or run it through flask:

> FLASK_APP=app.py flask run --host=0.0.0.0

Alternatively, run the convenience script:
> ./start.sh

To exit the VirtualEnvironment, use:
> deactivate

### 3.1 Run (Windows)

Enable the Virtual Environment for Goshna:
> .venv\Scripts\activate.bat

Set an environment variable. You can set this permanently in the Environment Variables for the System or User, or you can set it temporarily for each Command Prompt session using the following command (the 'set' command needs running for each newly opened CMD window):
> set PYTHONPATH=..

Run the application:
> python2 app.py

To exit the Virtual Environment after the application is closed, either close the CMD window or type the following:
> .venv\Scripts\deactivate.bat

## 4 Test running through uWSGI (localhost:5000)

Ensure the VirtualEnvironment is active:
> source flask/bin/activate

Ensure that uWSGI is installed:
> pip install uwsgi

Now run the application through uWSGI:
> PYTHONPATH=.. uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:application

## 5 PostgreSQL integration

Install PostgreSQL
> sudo apt-get install postgresql

Ensure Virtual Environment activated:
> source .venv/bin/activate

Install the Python module for connecting to the PostgreSQL database server:
> pip install psycopg2

Create the file `database-connection.ini` in the Server folder. Add the following contents to the file (updating the variables, such as the username and password where appropriate):
> [postgresql]  
> host=localhost  
> port=5432  
> database=YOUR-DB-NAME  
> user=YOUR-DB-USERNAME  
> password=YOUR-DB-PASSWORD  

Ensure a DB is created and a user with login privileges to that DB is also created. Update the `database-connection.ini` config file with the DB name, username, and password.
