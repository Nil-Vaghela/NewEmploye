from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import pandas as pd
import datetime
import openpyxl
import os
import random

app = Flask(__name__)
app.secret_key = 'nilvaghela'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class Admin(UserMixin):
    id = "admin"
    password = "32156"

def html_home_function():
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GSU CFA</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css">
    <style>
        body {{
            font-family: Arial, sans-serif;
            padding: 30px;
            min-height: 100vh;
            margin: 0;
            background: url('static/img4.jpg') no-repeat center center;
            background-size: cover;
            background-attachment: fixed;
        }}
        html {{
            min-height: 100vh;
        }}

        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}

        .header img {{
            width: 200px;
            border-radius: 100px;
            margin-bottom: 20px;
        }}

        .header h1 {{
            font-size: 22px;
            color: #333;
            text-shadow: 1px 1px 1px rgba(0, 0, 0, 0.1);
        }}

        .btn-primary {{
            background-color: #D70F26;
            border-color: #D70F26;
        }}

        .btn-primary:hover, .btn-primary:focus, .btn-primary:active {{
            background-color: #b90c1c;
            border-color: #b90c1c;
        }}

        .table-container table {{
            width: 100%;
            border-collapse: collapse;
            margin: 25px 0;
            font-size: 1.0em;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
            border-radius: 10px;
            overflow: hidden;
            font-weight : 600;

        }}

        .table-container th,
        .table-container td {{
            border: none;
            padding: 12px 15px;
        }}

        .table-container th {{
            background-color: #D70F26;
            color: #ffffff;
            text-align: left;
        }}

        .table-container tr:hover {{
            transform: scale(1.02);
            transition: transform 0.3s ease;
        }}

        .note-text {{
            text-align: center;
            color: #D70F26;
            font-size: 16px;
        }}

        .btn-spacing {{
            margin: 10px;
        }}

        .form-container {{
            margin-bottom: 30px;
        }}

        .form-group label {{
            font-weight: bold;
            color: #333;
        }}
        .table-container td:first-child {{
            font-size: 2em; 
        }}

    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <img src= 'static/LOGO.png' alt="GSU Logo">
        <h1>Where delicious meets delightful service.</h1>
    </div>
    <div class="form-container">
        <form method="post">
            <div class="form-group">
            <label for="username">User ID:</label>
            <input type="text" class="form-control" id="username" name="username" pattern="\d+" title="Please enter digits only" required>
            </div>
            <div class="form-group">
                <label>Action:</label>
                <select class="form-control" id="action" name="action">
                    <option value="Clock In">Clock In</option>
                    <option value="Clock Out">Clock Out</option>
                    <option value="Lunch End">Lunch End</option>
                    <option value="Lunch Start">Lunch Start</option>
                </select>
            </div>
            <button type="submit" class="btn btn-primary btn-spacing" onclick="return confirmAction()">Submit</button>
            <a href="admin" class="btn btn-primary btn-spacing">Admin Page</a>
            <a href="send_email" class="btn btn-primary btn-spacing">Send Email</a>
        </form>
    </div>
    
    <div class="table-container">
        
        {table}
        <p class="note-text">Made By Nil ❤️</p>
    </div>
</div>

<script>
    // Disable the back button
    history.pushState(null, document.title, location.href);
    window.addEventListener('popstate', function (event) {{
        history.pushState(null, document.title, location.href);
    }});

    function confirmAction() {{
        var action = document.getElementById("action").value;
        return confirm("Are you sure you want to " + action + "?");
    }}
</script>

</body>
</html>

'''

def Login_html_code():
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - GSU Attendance</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    <style>
        body {
            background-color: #f8f9fa;
            font-family: 'Roboto', Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            max-width: 400px;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1), 0 0 0 1px rgba(0, 0, 0, 0.1), 0 2px 2px rgba(0, 0, 0, 0.3);
            background-color: white;
        }
        .header {
            text-align: center;
            margin-bottom: 20px;
        }
        .header img {
            width: 50px;
            margin-bottom: 15px;
        }
        .header h1 {
            font-size: 24px;
            font-weight: bold;
            color: #D70F26;
        }
        .form-group label {
            font-weight: bold;
            color: #333;
        }
        .btn-primary {
            background-color: #D70F26;
            border-color: #D70F26;
        }
        .btn-primary:hover, .btn-primary:focus, .btn-primary:active {
            background-color: #b90c1c;
            border-color: #b90c1c;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <img src="https://commkit.gsu.edu/files/2019/06/PrimaryLogo3color-768x594.jpg" alt="GSU Logo" style="width: 50%;">
            <h1 class="text-center">GSU Attendance</h1>
        </div>
        <form method="POST">
            <div class="form-group">
                <label for="username">User ID</label>
                <input type="text" class="form-control" id="username" name="username" required>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" class="form-control" id="password" name="password" required>
            </div>
            <button type="submit" class="btn btn-primary btn-block">Login</button>
        </form>
    </div>
</body>
</html>
'''


def adminLogin():
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - GSU Admin Login</title>
    <style>
        html, body {
            min-height: 100vh;
        }
        body {
            background-color: #f8f9fa;
            font-family: 'Roboto', Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            max-width: 400px;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1), 0 0 0 1px rgba(0, 0, 0, 0.1), 0 2px 2px rgba(0, 0, 0, 0.3);
            background-color: white;
        }
        .header {
            text-align: center;
            margin-bottom: 20px;
        }
        .header img {
            width: 50px;
            margin-bottom: 15px;
        }
        .header h1 {
            font-size: 24px;
            font-weight: bold;
            color: #D70F26;
        }
        .form-group label {
            font-weight: bold;
            color: #333;
        }
        .btn-primary {
            background-color: #D70F26;
            border-color: #D70F26;
        }
        .btn-primary:hover, .btn-primary:focus, .btn-primary:active {
            background-color: #b90c1c;
            border-color: #b90c1c;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <img src="https://commkit.gsu.edu/files/2019/06/PrimaryLogo3color-768x594.jpg" alt="GSU Logo" style="width: 50%;">
            <h1 class="text-center">GSU Admin Login</h1>
        </div>
        <form method="POST">
            <div class="form-group">
                <label for="username">User ID</label>
                <input type="text" class="form-control" id="username" name="username" required>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" class="form-control" id="password" name="password" required>
            </div>
            <button type="submit" class="btn btn-primary btn-block">Login</button>
        </form>
    </div>
</body>
</html>
'''

def LoginCode():
    if request.method == 'POST':
        user_id = request.form['username']
        password = request.form['password']
        if user_id == Admin.id and password == Admin.password:
            login_user(Admin(), remember=True, duration=datetime.timedelta(hours=15))
            return redirect(url_for('index'))
        else:
            df = pd.read_excel('Employee Names.xlsx')

            for i in range(len(df)):
                # split the 'Name' field by spaces
                name_parts = df.loc[i, 'Name'].split()
                # take the first part of the name (i.e., the first name)
                first_name = name_parts[0]
                if first_name.lower() == user_id.lower() and str(df.loc[i, 'User ID']) == password:
                    # if first name and password match, login user and redirect to 'edit_points'
                    login_user(Admin(), remember=True, duration=datetime.timedelta(hours=15))
                    return redirect(url_for('edit_points', user_id=password))
            
        return "Invalid credentials. Please try again."

    return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - GSU Attendance</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    <style>
        body {
            background-color: #f8f9fa;
            font-family: 'Roboto', Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            max-width: 400px;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1), 0 0 0 1px rgba(0, 0, 0, 0.1), 0 2px 2px rgba(0, 0, 0, 0.3);
            background-color: white;
        }
        .header {
            text-align: center;
            margin-bottom: 20px;
        }
        .header img {
            width: 50px;
            margin-bottom: 15px;
        }
        .header h1 {
            font-size: 24px;
            font-weight: bold;
            color: #D70F26;
        }
        .form-group label {
            font-weight: bold;
            color: #333;
        }
        .btn-primary {
            background-color: #D70F26;
            border-color: #D70F26;
        }
        .btn-primary:hover, .btn-primary:focus, .btn-primary:active {
            background-color: #b90c1c;
            border-color: #b90c1c;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <img src="https://commkit.gsu.edu/files/2019/06/PrimaryLogo3color-768x594.jpg" alt="GSU Logo" style="width: 50%;">
            <h1 class="text-center">GSU Attendance</h1>
        </div>
        <form method="POST">
            <div class="form-group">
                <label for="username">User ID</label>
                <input type="text" class="form-control" id="username" name="username" required>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" class="form-control" id="password" name="password" required>
            </div>
            <button type="submit" class="btn btn-primary btn-block">Login</button>
            <p class="text-center note-text"> </p>
            <p class="text-center note-text">Made By Nil ❤️   V. 3.0.2</p>
        </form>
    </div>
</body>
</html>
'''
