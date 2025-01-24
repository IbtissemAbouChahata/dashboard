from django.shortcuts import render , redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
import psycopg2

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def login(request):
    if request.method == "POST":
        print("val read")
        # Get login credentials from POST request
        username = request.POST.get('Username')
        password = request.POST.get('Password')

        
        print("val non read")
        try:
            # Establish a connection to the PostgreSQL database for login check
            connection = psycopg2.connect(
                dbname="power",          # Replace with your database name
                user="postgres",         # Replace with your PostgreSQL username
                password="16082001",     # Replace with your PostgreSQL password
                host="localhost",        # Replace with your PostgreSQL host
                port="5432"              # Replace with your PostgreSQL port
            )

            # Create a cursor object for the login check
            cursor = connection.cursor()

            # Check if the username and password are valid in the users table
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchall()
            print(user)

            if user:
                # User is authenticated, proceed to fetch sensor data
                messages.success(request, "Login successful!")
                return redirect('app-index') # Call function to fetch sensor data
            else:
                # Authentication failed
                messages.error(request, "Invalid username or password.")
                return redirect('login')  # Redirect back to login page

        except psycopg2.Error as e:
            # Handle database connection errors
            print(f"Error connecting to PostgreSQL: {e}")
            messages.error(request, "Database connection error.")
            return redirect('login')

        finally:
            if connection:
                cursor.close()
                connection.close()

    # Render login page for GET request
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        full_name = request.POST.get('Name')
        print(full_name)
        username = request.POST.get('Username')
        print(username)
        password = request.POST.get('Password')
        print(password)
        confirm_password = request.POST.get('ConfirmPassword')
        print(confirm_password)

        # Simple validation checks
        if not full_name or not username or not password or not confirm_password:
            return render(request, 'user/signup.html', {'error': 'All fields are required'})

        if password != confirm_password:
            return render(request, 'user/signup.html', {'error': 'Passwords do not match'})

        try:
            # Connect to PostgreSQL database
            connection = psycopg2.connect(
                dbname="power",          # Replace with your database name
                user="postgres",         # Replace with your PostgreSQL username
                password="16082001",     # Replace with your PostgreSQL password
                host="localhost",        # Replace with your PostgreSQL host
                port="5432"              # Replace with your PostgreSQL port
            )
            cursor = connection.cursor()

            # Insert the user into your custom table
            insert_query = "INSERT INTO users (name, username, password) VALUES (%s, %s, %s);"
            cursor.execute(insert_query, (full_name, username, password))

            # Commit the transaction
            connection.commit()

            # Close the cursor and connection
            cursor.close()
            connection.close()

            return redirect('login')  # Redirect to the login page after signup

        except Exception as error:
            print(f"Error while connecting to PostgreSQL: {error}")
            return render(request, 'user/signup.html', {'error': 'Failed to sign up'})

    return render(request, 'user/signup.html')