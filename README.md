
# DjangoCon Africa 2023 Grants Application Emailer

This Python script automates the process of sending emails to grant applicants for DjangoCon Africa 2023 using Google Sheets and the SendGrid API.

## Prerequisites

Before running either of the provided scripts, make sure you have the following prerequisites in place:

1. Python: Ensure you have Python installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

2. Required Python Libraries: Install the necessary Python libraries using pip by running the following command:

   ```
   pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib sendgrid-python python-dotenv
   ```

3. Google Sheets API Credentials: Create a service account and obtain a JSON key file for accessing Google Sheets. Update the JSON key file path in your environment variables or directly in the script.

4. Google Sheets Setup: Create a Google Sheets spreadsheet with the applicants' data and grant status. Make sure you have the Google Sheets spreadsheet ID.

5. SendGrid API Key: Sign up for a SendGrid account and generate an API key. Set the API key in your environment variables.

6. Environment Variables: Create a `.env` file in the project directory and set the following environment variables:

   ```
   FOLDER_ID=your_folder_id
   SPREADSHEET_ID=your_spreadsheet_id
   SENDGRID_API_SECRET=your_sendgrid_api_secret
   SENDGRID_EMAIL_SENDER=your_sendgrid_email_sender
   SENDGRID_SENDER_NAME=your_sendgrid_sender_name
   SENDGRID_SUBJECT=your_sendgrid_email_subject
   GOOGLE_CREDENTIALS=your_path_to_google_credentials_json
   ```

## Usage

### Google Sheets Structure

The Google Sheets used in this project is structured with the following columns:

- `fullname`: The full name of the grant applicant.
- `email`: The email address of the grant applicant.
- `status`: The status of the email communication with the applicant, which can have one of the following values:
  - `SENT`: Indicates that the email was successfully sent to the applicant.
  - `PENDING`: Indicates that the email has not yet been sent and is awaiting processing.
  - `FAILED`: Indicates that the email sending process encountered an issue and was not successful.

Here is an example of how the Google Sheets data may look:

|   fullname   |          email         |  status  |
|--------------|------------------------|----------|
| Mia Gomez    | mia.gomez@gmail.com    | SENT     |
| Sora Kim     | sora.kim@gmail.com     | PENDING  |
| John Doe     | john.doe@example.com   | FAILED   |

You should ensure that your Google Sheets follows this structure for the script to work correctly. The script will read data from the `fullname` and `email` columns and update the `status` column with one of these values based on the email sending process.



### Batch Email Sending (First Script)

1. Run the first script using the following command:

   ```
   python batch_email_script.py
   ```

2. The script will fetch applicant data from the Google Sheets, slice it into batches, and send rejection emails to applicants using SendGrid.

3. The status of each email (SENT or FAILED) will be updated in the Google Sheets.

### One-at-a-Time Email Sending (Second Script)

1. Run the second script using the following command:

   ```
   python single_email_script.py
   ```

2. The script will send rejection emails to each applicant one at a time, updating the Google Sheets with the email status for each applicant.

3. To avoid rate limits, the script includes a delay every 50 emails (adjustable as needed).

## Email Template

The rejection email template is located within each script and can be customized to suit your needs. You can modify the HTML content in the `email` function to change the email's content and formatting.

## Contributing

Feel free to contribute to this project by submitting issues or pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Make sure to replace `batch_email_script.py` and `single_email_script.py` with the actual names of your Python scripts. Additionally, provide the necessary details and instructions specific to your project as needed.
