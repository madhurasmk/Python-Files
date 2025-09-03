from flask import Flask, request, render_template_string
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

# Route to display the form
@app.route('/')
def form():
    return render_template_string(open('SurveyForm.html').read())

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit_form():
        can_name = request.form["candidatename"]
        can_college = request.form["college"]
        can_email = request.form["candidateemail"]
        # gradYear1 = getSelectedRadio('gradYear')
        # position1 = getSelectedRadio('position')
        # workauth1 = getSelectedRadio('workauth');
        # salary = document.getElementById("salary").value.trim();
        # availability = document.getElementById("offered").value.trim();
        # timeframe = document.getElementById("timeframe").value.trim();
    # Compose the email
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "New Contact Form Submission"
        msg['From'] = '@gmail.com'
        msg['To'] = '@gmail.com'

    # Create the body of the email
        html_content = f"""
        <html>
        <body>
            <h2>New Contact Form Submission</h2>
            <p><strong>Name:</strong> {can_name}</p>
            <p><strong>Email:</strong> {can_college}</p>
            <p><strong>Message:</strong><br>{can_email}</p>
        </body>
        </html>
        """
        msg.attach(MIMEText(html_content, 'html'))

        # Send the email
        try:
            with smtplib.SMTP('smtp.gmail.com', 465) as server:
                server.starttls()
                server.login('@gmail.com', '')
                server.sendmail(msg['From'], msg['To'], msg.as_string())
            return "Form submitted successfully!"
        except Exception as e:
            return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)
