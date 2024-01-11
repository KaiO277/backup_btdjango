from django.core.mail import EmailMessage
from django.conf import settings
import smtplib

def send_email(subject, message, recipient_list):
    """
    Hàm gửi email bằng SMTP.
    
    Parameters:
    - subject: Tiêu đề của email.
    - message: Nội dung của email.
    - recipient_list: Danh sách người nhận email.
    """
    try:
        email = EmailMessage(
            subject, 
            message,
            settings.EMAIL_HOST_USER, 
            [recipient_list])
        email.send(fail_silently=False)
        print("Email sent successfully.")
    except smtplib.SMTPException as e:
        print(f"Error sending email: {e}")


























# import smtplib

# from email.message import EmailMessage

# from django.conf import settings

# def send_email(subject, message, recipient_list):

#     # Tạo một đối tượng EmailMessage

#     msg = EmailMessage()

#     msg.set_content(message)

#     msg['Subject'] = subject

#     msg['From'] = settings.EMAIL_HOST_USER

#     msg['To'] = ', '.join(recipient_list)

#     # Kết nối đến máy chủ SMTP và gửi email

#     with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as smtp:

#         smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

#         smtp.send_message(msg)