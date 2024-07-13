from flask import Flask, render_template, request, redirect, url_for, flash
import gspread
from google.oauth2.service_account import Credentials
import boto3
import botocore
import json
import urllib.request

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

# S3 bucket details
s3_bucket_url = 'https://mywebsite-images-bucket.s3.ap-south-1.amazonaws.com'
s3_key = 'mywebsite-linux-dd758754bf56.json'

# Function to retrieve JSON credentials from S3
def get_credentials_from_s3(bucket_url, key):
    try:
        url = f"{bucket_url}/{key}"
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        return data
    except Exception as e:
        print(f"Error retrieving credentials from S3: {str(e)}")
        return None

# Initialize Google Sheets client
def initialize_google_sheets(credentials):
    try:
        scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_info(credentials, scopes=scope)
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        print(f"Error initializing Google Sheets client: {str(e)}")
        return None

# Retrieve Google Sheets client
credentials = get_credentials_from_s3(s3_bucket_url, s3_key)
if credentials:
    gc = initialize_google_sheets(credentials)
    if not gc:
        raise ValueError("Failed to initialize Google Sheets client")
else:
    raise ValueError("Failed to retrieve credentials from S3")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/diary')
def diary():
    return render_template('diary.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['e-mail']
        message = request.form['message']

        try:
            # Store data in Google Sheets
            store_in_google_sheets(first_name, last_name, email, message)
            flash('Your message has been sent successfully!', 'success')
            return redirect(url_for('contact'))
        except Exception as e:
            flash(f'Error storing data: {str(e)}', 'error')
            return redirect(url_for('contact'))

    return render_template('contact.html')

def store_in_google_sheets(first_name, last_name, email, message):
    try:
        spreadsheet = gc.open('MWL')
        worksheet = spreadsheet.sheet1  # Use sheet1 or specify a sheet name
        row = [first_name, last_name, email, message]
        worksheet.append_row(row)
    except Exception as e:
        print(f"Error storing data in Google Sheets: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
