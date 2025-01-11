import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class mailresult:

# Function to send an email
    def send_email(self,to_address, subject, body):
     # Your email credentials
        sender_email = "zerobreyncells@gmail.com"
        sender_password = "rwdpfigtbbvjvvzd"
    
    # SMTP server configuration (for Gmail, use smtp.gmail.com)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
    
    # Prepare email content
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_address
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
    
    # Send the email
        server.sendmail(sender_email, to_address, msg.as_string())
        server.quit()

# Function to process the CSV and send emails
    def process_csv_and_send_emails(self,csv_file):
        with open(csv_file, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
            # Get student's name, email, marks, subject details
                name = row['Name']
                email = row['Email']
                total_marks = row['Total']
                q1_marks = row['Q1_Marks']
                q2_marks = row['Q2_Marks']
                q3_marks = row['Q3_Marks']
                q4_marks = row['Q4_Marks']
                subject_id = row['SubjectID']
                subject_name = row['SubjectName']
            
            # Create the email content
                subject = f"Your Marks for {subject_name} ({subject_id})"
                body = f"Dear {name},\n\nYour marks for the subject '{subject_name}' (Subject ID: {subject_id}) are as follows:\n\n"
                body += f"Q1: {q1_marks}\nQ2: {q2_marks}\nQ3: {q3_marks}\nQ4: {q4_marks}\n"
                body += f"\nTotal Marks: {total_marks}\n\nBest regards,\nYour University"
            
            # Send the email
                self.send_email(email, subject, body)
                print(f"Email sent to {name} ({email})")

# Example usage
mail=mailresult()
csv_file = r'students_data.csv'  # Update with the actual CSV file path
mail.process_csv_and_send_emails(csv_file)
