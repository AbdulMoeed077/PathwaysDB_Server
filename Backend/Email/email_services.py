import smtplib
from email.mime.text import MIMEText
from fastapi import HTTPException

def send_email(smtp_server: str, smtp_port: int, smtp_username: str, smtp_password: str, from_email: str, to_email: str, msg: MIMEText):
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
    except smtplib.SMTPException as e:
        # Handle SMTP errors
        raise HTTPException(status_code=400, detail=f"SMTP Error: {str(e)}")
    except ConnectionRefusedError as e:
        # Handle connection refused error
        raise HTTPException(status_code=400, detail="Connection to SMTP server was actively refused.")
    except Exception as e:
        # Handle other exceptions
        raise HTTPException(status_code=400, detail=f"Error sending email: {str(e)}")
