import os
from mailjet_rest import Client
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('MAILJET_API_KEY')
api_secret = os.getenv('MAILJET_SECRET_KEY')
sender_email = os.getenv('SENDER_EMAIL')

mailjet = Client(auth=(api_key, api_secret), version='v3.1')


def send_application_confirmation(applicant_email, applicant_name, job_title, application_id):
    """Send confirmation email to applicant"""
    
    data = {
        'Messages': [
            {
                "From": {
                    "Email": sender_email,
                    "Name": "Jovian Careers"
                },
                "To": [
                    {
                        "Email": applicant_email,
                        "Name": applicant_name
                    }
                ],
                "Subject": f"Application Received - {job_title}",
                "HTMLPart": f"""
                <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                        <h2 style="color: #4a90e2;">Application Received! ✅</h2>
                        
                        <p>Hi {applicant_name},</p>
                        
                        <p>Thank you for applying for the <strong>{job_title}</strong> position!</p>
                        
                        <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                            <p style="margin: 0;"><strong>Application ID:</strong> #{application_id}</p>
                            <p style="margin: 10px 0 0 0;"><strong>Status:</strong> Under Review</p>
                        </div>
                        
                        <p>We'll review your application and get back to you soon.</p>
                        
                        <p style="margin-top: 30px;">Best regards,<br>
                        <strong>Jovian Careers Team</strong></p>
                    </div>
                </body>
                </html>
                """
            }
        ]
    }
    
    try:
        result = mailjet.send.create(data=data)
        if result.status_code == 200:
            print(f"✅ Email sent to {applicant_email}")
            return True
        else:
            print(f"❌ Failed to send email. Status: {result.status_code}")
            print(f"Response: {result.json()}")
            return False
    except Exception as e:
        print(f"❌ Error sending email: {str(e)}")
        return False


def send_admin_notification(applicant_name, applicant_email, job_title, application_id):
    """Send notification to admin (yourself)"""
    
    data = {
        'Messages': [
            {
                "From": {
                    "Email": sender_email,
                    "Name": "Jovian Careers System"
                },
                "To": [
                    {
                        "Email": sender_email,  # Send to yourself
                        "Name": "Admin"
                    }
                ],
                "Subject": f"New Application: {applicant_name} - {job_title}",
                "HTMLPart": f"""
                <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                        <h2 style="color: #4a90e2;">New Application Received! 🎉</h2>
                        
                        <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                            <p><strong>Applicant:</strong> {applicant_name}</p>
                            <p><strong>Email:</strong> <a href="mailto:{applicant_email}">{applicant_email}</a></p>
                            <p><strong>Job:</strong> {job_title}</p>
                            <p><strong>Application ID:</strong> #{application_id}</p>
                        </div>
                        
                        <a href="http://localhost:5000/admin/applications" 
                           style="display: inline-block; background: #4a90e2; color: white; padding: 10px 20px; 
                                  text-decoration: none; border-radius: 5px; margin-top: 10px;">
                            View All Applications
                        </a>
                    </div>
                </body>
                </html>
                """
            }
        ]
    }
    
    try:
        result = mailjet.send.create(data=data)
        if result.status_code == 200:
            print(f"✅ Admin notification sent to {sender_email}")
            return True
        else:
            print(f"❌ Failed to send admin notification. Status: {result.status_code}")
            print(f"Response: {result.json()}")
            return False
    except Exception as e:
        print(f"❌ Error sending admin notification: {str(e)}")
        return False