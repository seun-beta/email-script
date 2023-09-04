import json
import time
import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


load_dotenv()  # take environment variables from .env

folder_id = os.environ["FOLDER_ID"]
spreadsheet_id = os.environ["SPREADSHEET_ID"]
sendgrid_api_secret = os.environ["SENDGRID_API_SECRET"]
sendgrid_email_sender = os.environ["SENDGRID_EMAIL_SENDER"]
sendgrid_sender_name = os.environ["SENDGRID_SENDER_NAME"]
sendgrid_subject = os.environ["SENDGRID_SUBJECT"]
auth_json = os.environ["GOOGLE_CREDENTIALS"]
acct_json = json.loads(auth_json)

creds = service_account.Credentials.from_service_account_info(acct_json)

service = build("sheets", "v4", credentials=creds)


def fetch_applicants_from_sheet():
    ranges = "A2:B"
    result = (
        service.spreadsheets()
        .values()
        .batchGet(spreadsheetId=spreadsheet_id, ranges=ranges)
        .execute()
    )
    ranges = result.get("valueRanges", [])
    sheet_data = result["valueRanges"][0]["values"]

    return sheet_data


def update_value(value, range_name):
    value_input_option = "USER_ENTERED"
    values = [[value]]
    body = {"values": values}
    result = (
        service.spreadsheets()
        .values()
        .update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption=value_input_option,
            body=body,
        )
        .execute()
    )
    return result


def email(email, fullname):
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        
            <style>
                body  {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    background-color: #f6f6f6;
                    padding: 20px;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #fff;
                    border-radius: 5px;
                    padding: 20px;
                    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                }}

                p {{
                    margin-bottom: 10px;
                }}

                .link {{
                    color: #000000;
                    font-size: medium;
                }}

                .social-links {{
                    text-align: center;
                    margin-top: 30px;
                }}

                .social-links a {{
                    display: inline-block;
                    margin: 0 10px;
                    color: #000000;
                    text-decoration: none;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <p>Dear {fullname},</p>
                <p>On behalf of the DjangoCon Africa 2023 Grants committee, we regret 
                    to inform you that your grant application has not been approved to attend DjangoCon 
                    Africa this year. 
                </p>
                <p>The applicant pool was large and unfortunately we are unable to fund 
                    all grant requests at this time. Thank you for the time and effort you committed to submitting your application.
                </p>
                <p>Sincerely,<br>DjangoCon Africa 2023 Grants Committee</p>
                <br>
                <div class="social-links">
                    <a href="[Link to Facebook]" target="_blank">Facebook</a>
                    <a href="[Link to Twitter]" target="_blank">Twitter</a>
                    <a href="[Link to Instagram]" target="_blank">Instagram</a>
                    <a href="[Link to LinkedIn]" target="_blank">LinkedIn</a>
                </div>
                <br>
            </div>
        </body>
    </html>
    """
    message = Mail(
        from_email=(sendgrid_email_sender, sendgrid_sender_name),
        to_emails=email,
        subject=sendgrid_subject,
        html_content=html,
    )
    try:
        sg = SendGridAPIClient(api_key=sendgrid_api_secret)
        sg.send(message)
        return "SENT"
    except Exception as e:
        return "FAILED"


def send_email():
    applicants = fetch_applicants_from_sheet()
    value = 2

    for applicant in applicants:
        response = email(fullname=applicant[0], email=applicant[1])
        update_value(value=response, range_name=f"C{value}")
        range_value += 1
        if range_value % 50 == 0:
            time.sleep(60)


send_email()
