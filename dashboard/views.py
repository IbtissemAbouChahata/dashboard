1# views.py
import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from .models import EnvironmentalData
from django.db import connection
import psycopg2
import json
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
def login(request):
    return render(request, 'user/login.html')

def signup(request):
    return render(request, 'user/signup.html')

def home(request):
    return render(request, 'home.html')
def defdetect(request):
    return render(request, 'detection.html')

import psycopg2

def fetch_data(request):
    connection = None
    cursor = None
    try:
        # Establish a connection to the PostgreSQL database
        connection = psycopg2.connect(
            dbname="power",
            user="postgres",
            password="16082001",
            host="localhost",
            port="5432"
        )

        # Create a cursor object using the cursor() method
        cursor = connection.cursor()

        # Execute a SQL query using the execute() method
        cursor.execute("SELECT * FROM sensor_data;")

        # Fetch and return the result of the query
        result = cursor.fetchall()[-15:]

        # Extract data into separate lists or dictionaries
        labels = []
        values1 = []
        values2 = []
        values3 = []
        values4 = []
        values5 = []

        for row in result:
            # Convert the first column (assumed to be a date) to a string if it's a date or datetime object
            labels.append(str(row[0]))  # Convert to string if needed
            values1.append(row[1])
            values2.append(row[2])
            values3.append(row[3])
            values4.append(row[4])
            values5.append(row[5])

        # Pass the data to the template
        return render(request, 'index.html', {
            'labels': json.dumps(labels),
            'values1': json.dumps(values1),
            'values2': json.dumps(values2),
            'values3': json.dumps(values3),
            'values4': json.dumps(values4),
            'values5': json.dumps(values5),
        })

    except Exception as error:
        print(f"Error connecting to PostgreSQL database: {error}")
        return render(request, 'index.html', {'message': 'Error fetching data from the database.'})

    finally:
        # Close the cursor and connection to clean up
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        print("PostgreSQL connection is closed")
@csrf_exempt
def add_value(request):
    if request.method == 'POST':
        # Retrieve form data
        temperature = request.POST.get('Temperature')
        humidity = request.POST.get('Humidity')
        voltage = request.POST.get('Voltage')
        current = request.POST.get('Current')
        luminosity = request.POST.get('Luminosity')
        auto_date = request.POST.get('autoDate')
        print(type(voltage))
        temperature = float(temperature)
        humidity = float(humidity)
        voltage = float(voltage)
        current = float(current)
        luminosity = float(luminosity)
        print(type(voltage))
            # Establish a connection to the PostgreSQL database
        connection = psycopg2.connect(
            dbname="power",          # Replace with your database name
                user="postgres",         # Replace with your PostgreSQL username
                password="16082001",    # Replace with your PostgreSQL password
                host="localhost",       # Replace with your PostgreSQL host, usually 'localhost'
                port="5432"             # Replace with your PostgreSQL port, usually 5432
            )

            # Create a cursor object
        cursor = connection.cursor()

            # Execute a SQL query(
        cursor.execute ("""INSERT INTO sensor_data (timestamp, temperature, humidity, voltage, current, luminosity) VALUES (%s,%s,%s,%s,%s,%s);""",(auto_date,temperature,humidity,voltage,current,luminosity))  # Replace with your actual SQL query

            # Commit the transaction
        connection.commit()

            # Return success response
        return redirect('app-index')
    

def fetch_latest_value(request):
    try:
        # Establish a connection to the PostgreSQL database
        connection = psycopg2.connect(
            dbname="power",
            user="postgres",
            password="16082001",
            host="localhost",
            port="5432"
        )

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 1;")
        result = cursor.fetchone()
        print(result)
        
        if result:
            latest_timestamp = result[0]
            latest_temperature = result[1]
            latest_humidity = result[2]
            latest_voltage = result[3]
            latest_current = result[4]
            latest_luminosity = result[5]
        else:
            latest_timestamp = 'No data'
            latest_temperature = 'No data'
            latest_humidity = 'No data'
            latest_voltage = 'No data'
            latest_current = 'No data'
            latest_luminosity = 'No data'

        # Pass the data to the template
        return render(request, 'index.html', {
            'latest_timestamp': latest_timestamp,
            'latest_temperature': latest_temperature,
            'latest_humidity': latest_humidity,
            'latest_voltage': latest_voltage,
            'latest_current': latest_current,
            'latest_luminosity': latest_luminosity
        })

    except Exception as error:
        print(f"Error connecting to PostgreSQL database: {error}")
        return render(request, 'index.html', {'message': 'Error fetching data from the database.'})

    finally:
        # Close the cursor and connection to clean up
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        print("PostgreSQL connection is closed")