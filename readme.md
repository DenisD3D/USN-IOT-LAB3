# Internet of Things and Cybersecurity
## 	Lab 3 - Industry 4.0 and Cybersecurity - University of South Eastern Norway

Project goal:
- Control an air heater model using a USB-6008 DAQ (control application)
- Save the data to a database (data application, communication with control application through MQTT)
- Visualize the data (dashboard application)

All commands are given relative to the root repository folder (IOT3).

## 1. Control application
The control application is written in Python. To run the application, install the required dependencies using the following command:
```bash
pip install -r requirements.txt
```
Then fill the required credentials in the .env file:
```bash
cp control-application/.env.example control-application/.env
```
To find PID parameters using the Ziegler-Nichols method, run the following command:
```bash
python control-application/ziegler_nichols.py
```
To run the control application using the simulation model, run the following command:
```bash
python control-application/simulated_control.py
```
To run the control application using the real air heater, run the following command:
```bash
python control-application/real_control.py
```

## 2. Data application
The Database application is written in Python. To run the application, install the required dependencies using the following command:
```bash
pip install -r requirements.txt
```
Then fill the required credentials in the .env file:
```bash
cp data-application/.env.example data-application/.env2
```
To run the database application, run the following command:
```bash
python data-application/database.py
```

## 3. Dashboard application
The dashboard application is a Laravel website written in PHP. 
First, copy the .env.example file to .env and change the database settings to match your database settings (Postgresql is used in this project).
```bash
cp dashboard-application/.env.example dashboard-application/.env
```
```ini
DB_CONNECTION=pgsql
DB_HOST=
DB_PORT=
DB_DATABASE=
DB_USERNAME=
DB_PASSWORD=
```
Then install the required dependencies and generate the dependencies using the following commands:
```bash
cd dashboard-application
composer install
php artisan key:generate
php artisan migrate
```

To start the dashboard application locally, run the following command:
```bash
cd dashboard-application
php artisan serve
```

The dashboard application uses the Jetstream package for authentication. 
The file created or edited for this project are
- app/Models/Temperature.php
- app/LaravelCharts.php (edited to support shorter time intervals)
- routes/web.php
- resources/views/dashboard.blade.php
- resources/views/components/application-logo.blade.php
- resources/views/components/application-mark.blade.php
- resources/views/auth/login.blade.php
- resources/views/auth/register.blade.php
- database/migrations/2023_10_24_131431_create_temperatures_table.php

For demonstration purposes, users can create their own account and view the dashboard. To disable account creation in the case of a real application, comment out the following lines in config/fortify.php:
```php
'features' => [
    Features::registration(), // <--- comment out this line
    ...
],
```

To push the application to heroku for deployment, run the following commands:
```bash
git subtree push --prefix dashboard-application heroku main 
```

The dashboard application is deployed at https://usn-iot-lab3-332c197a7e45.herokuapp.com/