# Import necessary modules and classes
from fastapi import HTTPException, Depends, APIRouter, Query
from fastapi.security import OAuth2PasswordRequestForm
from Auth import auth_models
from Auth import auth_services
from starlette.responses import JSONResponse

# Create an APIRouter instance
router = APIRouter()

# Function to get the current user and authorize based on the token
async def get_current_user(current_user: auth_models.User = Depends(auth_services.authenticate_user)):
    return current_user

# Endpoint for user registration (requires token-based authentication)
@router.post("/register_user/")
def register_user(user: auth_models.UserCreate):
    try:
        # Call the register_user function from auth_services
        auth_services.register_user(user)
        return True
    except Exception as e:
        # Handle exceptions and return an HTTP error response
        raise HTTPException(status_code=400, detail=f"{str(e.detail)}")

# Endpoint for verifying email (requires token-based authentication)
@router.get("/verify_email", response_class=JSONResponse)
def verify_email(token: str = Query(..., description="Verification token from the email link")):
    try:
        # Call the verify_email function from auth_services
        auth_services.verify_email_token(token)
        return True
    except Exception as e:
        # Handle exceptions and return an HTTP error response
        raise HTTPException(status_code=400, detail=f"{str(e.detail)}")

# Endpoint for sending a reset password link (requires token-based authentication)
@router.get("/send_reset_password_link", response_class=JSONResponse)
def send_reset_password_link(email: str = Query(...)):
    try:
        # Call the verify_email function from auth_services
        auth_services.send_reset_password_link(email)
        return True
    except Exception as e:
        # Handle exceptions and return an HTTP error response
        raise HTTPException(status_code=400, detail=f"Could not reset the password check your email: {str(e.detail)}")

# Endpoint for resetting the password (requires token-based authentication)
@router.get("/reset_password", response_class=JSONResponse)
def reset_password(password: str = Query(...), token: str = Query(...)):
    try:
        # Call the reset funct from auth_services
        auth_services.reset_password(password, token)
        return True
    except Exception as e:
        # Handle exceptions and return an HTTP error response
        raise HTTPException(status_code=400, detail=f"Could not reset the password: {str(e.detail)}")

# Endpoint for reading all users (requires token-based authentication)
@router.get("/read_all_user/", response_model=list[auth_models.User])
def read_all_users(skip: int = 0, limit: int = 100, current_user: auth_models.User = Depends(auth_services.authenticate_user)):
    try:
        # Call the display_all_users function from auth_services
        db_user = auth_services.display_all_users(skip=skip, limit=limit)
        return db_user
    except Exception as e:
        # Handle exceptions and return an HTTP error response
        raise HTTPException(status_code=400, detail=f"Error while getting user from database: {str(e.detail)}")

# Endpoint for user login and access token generation (does not require authentication)
@router.post("/", response_model=auth_models.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        # Call the login_for_access_token function from auth_services
        login = auth_services.login_for_access_token(form_data=form_data)
        return login
    except Exception as e:
        # Handle exceptions and return an HTTP error response
        raise HTTPException(status_code=400, detail=f"{e.detail}")

# Endpoint for getting the current user
@router.get("/get_current_user/", response_model=auth_models.User)
async def get_current_user(current_user: auth_models.User = Depends(auth_services.authenticate_user)):
    return current_user
