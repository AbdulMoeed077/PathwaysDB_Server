# Import necessary modules and classes
from fastapi import Depends, HTTPException, status
from jinja2 import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt, JWTError
from Database.Repository.User_Repository import UserRepository
from Auth import auth_models
from Email import email_services

# Constants for authentication
SECRET_KEY = "thequickbrownfoxjumpsoverthelazydog"
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 2400
token = ""
emailmessage = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Email Verification</title>
        </head>
        <body>
            <p>Hello {{to_email}},</p>
            
            <p>Thank you for signing up! To complete your registration, please click the link below:</p>
            <p><a href="http://localhost:5173/verifyEmail?token={{verification_token}}">Verify Email</a></p>
            
            <p>If you didn't sign up for this service, you can safely ignore this email.</p>
            
            <p>Best regards,<br>Your Name</p>
        </body>
        </html>
    """
forgetpasswordmessage = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Reset Password</title>
        </head>
        <body>
            <p>Hello {{fname}} {{lname}},</p>
            
            <p>Please click the link below to reset your password:</p>
            <p><a href="http://localhost:5173/resetPassword?token={{verification_token}}">Verify Email</a></p>
            
            <p>If you didn't sign up for this service, you can safely ignore this email.</p>
            
            <p>Best regards,<br>Your Name</p>
        </body>
        </html>
    """


# Create an OAuth2 password bearer token scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="Auth")

# Create a password context for hashing and verifying passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to generate an email verification token
def generate_email_verification_token(user: auth_models.User):
    try: 
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"id": user.id, "email": user.email, "scopes": user.roles }, expires_delta=access_token_expires)
        return access_token
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e.detail}")



# Function to send a verification email
def send_verification_email(email, verification_token, message, fname, lname):
    # Email configuration (SMTP)
    smtp_server = "smtp.gmail.com"  # Replace with your SMTP server
    smtp_port = 587   # Replace with your SMTP port
    smtp_username = "moedashfaq@gmail.com"  # Replace with your SMTP username
    smtp_password = "iwezputfvsuwvqrs"  # Replace with your SMTP password
    from_email = "moedashfaq@gmail.com"
    to_email = email

    # Email message template (HTML)

    # Render the email template with values
    template = Template(message)
    rendered_template = template.render(fname=fname, lname=lname, verification_token=verification_token)

    # Email subject
    subject = "Verify Your Email"

    # Create an email message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(rendered_template, 'html'))

    try:
        # Send the email using email_services (replace with your actual email service)
        email_services.send_email(smtp_server, smtp_port, smtp_username, smtp_password, from_email, to_email, msg)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error while sending email. {e.detail}")

# Function to display all users with pagination
def display_all_users(skip: int, limit: int, token:str = Depends(oauth2_scheme)):
    try:
        # Call UserRepository's get_users function to retrieve users from the database
        
        db_user = UserRepository.get_users(skip=skip, limit=limit)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e.detail}")

# Function to authenticate a user against the database
def send_reset_password_link(email: str):
    try:
        # Call UserRepository's get_users function to retrieve users from the database
        db_user = UserRepository.get_user_by_email(email)
        if db_user:
            try:
                verification_token = generate_email_verification_token(db_user)
                send_verification_email(db_user.email, verification_token, forgetpasswordmessage, db_user.fname, db_user.lname)
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"{e.detail}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e.detail}")

def reset_password(password: str, token: str):
    try:
        db_user = authenticate_user(token)
        if(db_user):
            try:
                db_user = UserRepository.update_password(db_user.id, password)
                return db_user
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"{e.detail}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e.detail}")

    
# Function to register a new user
def register_user(user: auth_models.UserCreate):
    try:
        # Create a new user in the database and send a verification email
        db_user = UserRepository.create_user_in_db(user)
        verification_token = generate_email_verification_token(db_user)
        send_verification_email(db_user.email, verification_token, emailmessage, db_user.fname, db_user.lname)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e.detail}")

# Function to verify email and activate user
def verify_email_token(token: str):
    try:
        # Authenticate the user validation and mark them as verified
        db_user = authenticate_user(token)
        db_user = UserRepository.update_is_verified(db_user.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e.detail}")

# Function to authenticate a user with role validation
def authenticate_user(token:str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode and verify the JWT token and retrieve the username and role
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        scope_role: str = payload.get("scopes")
        if email is None:
            raise credentials_exception
    except JWTError as e:
        raise HTTPException(status_code=400, detail=e)
    # Retrieve the user from the database based on the username
    user = UserRepository.get_user_by_email(email=email)
    # Validate user roles against the provided scope
    authorize_scopes = authorize_user_scopes(user, scope_role)
    if not authorize_scopes:
        raise credentials_exception
    if user is None:
        raise credentials_exception
    return user

# Function to verify password
def verify_password(plain_password, password):
    return pwd_context.verify(plain_password, password)

# Function to authenticate a user against the database and check if the given password is correct
def authenticate_db_user(email: str, password: str):
    user = UserRepository.get_user_by_email(email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user

# Function to create an access token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error while creating token.")

# Function to authorize user roles
def authorize_user_scopes(user: auth_models.User, form_data: list[str]):
    # Check if the user's roles contain the required scope
    for scope in form_data:
        if not any(role == scope for role in user.roles):
            raise Exception(f"{form_data.scopes} does not found in {user.roles} projects.", status_code=401)
    return True

# Function to login and generate an access token
def login_for_access_token(form_data: OAuth2PasswordRequestForm):
    try:
        # Check if the user is present in the database and provided valid credentials
        user = authenticate_db_user(form_data.username, form_data.password)
        if user:
            if user.is_active:
                try:
                    # Authorize user scopes and create an access token
                    authorize_scopes = authorize_user_scopes(user, form_data.scopes)
                    if authorize_scopes:
                        try:
                            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                            access_token = create_access_token(data={"id": user.id,"email": user.email ,"scopes": user.roles}, expires_delta=access_token_expires)
                            return {"access_token": access_token, "token_type": "bearer"}
                        except Exception as error:
                            raise HTTPException(status_code=400, detail=f"{error.detail}")
                    else:
                        raise HTTPException(status_code=400, detail=f"User does not have the authorized scopes.")
                except Exception as error:
                    raise HTTPException(status_code=400, detail=f"Error Authorizing scopes")
            else:
                raise HTTPException(status_code=400, detail=f"Email is not verified.")
        else:
            raise HTTPException(status_code=400, detail=f"Invalid Email or Password.", headers={"WWW-Authenticate": "Bearer"})
    except Exception as error:
       raise HTTPException(status_code=400, detail=f"{error.detail}")