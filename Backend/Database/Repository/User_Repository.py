# Import necessary modules and classes
from fastapi import HTTPException
from passlib.hash import bcrypt
from sqlalchemy.orm import Session
from Auth import auth_models
from Database.DB_Models import DB_User
from Database.SqlAlchemy import engine
from sqlalchemy.orm import joinedload
from Database.DB_Models.DB_Role import Role_DB

class UserRepository:
    # Function for creating a new user in the database
    def create_user_in_db(user: auth_models.UserCreate):
        try:
            with Session(engine) as session:
                # Check if a user with the same email already exists
                db = session.query(DB_User.User).filter(DB_User.User.email == user.email).first()

                if not db:
                    # Hash the user's password
                    password = bcrypt.hash(user.password)

                    # Create a new user object
                    db_user = DB_User.User(
                        email=user.email,
                        password=password,
                        fname=user.fname,
                        lname=user.lname,
                        is_active=user.is_active
                    )

                    # Fetch the "user" role from the database
                    db_roles = session.query(Role_DB).filter(Role_DB.name == "user").first()

                    # Associate the "user" role with the user
                    db_user.roles.append(db_roles)
                    # Add the user to the database
                    session.add(db_user)
                    session.commit()

                    # Refresh the user object to get its updated state
                    session.refresh(db_user)

                    user_return=auth_models.UserRoles(
                        id=db_user.id,
                        email=db_user.email,
                        password=db_user.password,
                        fname=db_user.fname,
                        lname=db_user.lname,
                        is_active=db_user.is_active
                    )
                    for roles in db_user.roles:
                        user_return.roles.append(roles.name)

                    return user_return
                else:
                    # Raise an exception if a user with the same email already exists
                    raise HTTPException
        except Exception:
            # Handle any exceptions that occur during the process
            raise HTTPException(status_code=400, detail=f"User with email '{user.email}' already exists in the database.")
        
    # Function for updating the 'is_active' status of a user
    def update_is_verified(user_id: str):
        try:
            with Session(engine) as session:
                user = session.query(DB_User.User).filter(DB_User.User.id == user_id).first()
                if user:
                    user.is_active = True
                    session.commit()
                db_user = DB_User.User(
                    email=user.email,
                    fname=user.fname,
                    lname=user.lname,
                    is_active=user.is_active
                )
                return db_user
        except Exception:
            raise HTTPException(status_code=400, detail=f"Error while updating the user to varified.")
    
    def update_password(user_id: str, password: str):
        try:
            with Session(engine) as session:
                user = session.query(DB_User.User).filter(DB_User.User.id == user_id).first()
                hash_password = bcrypt.hash(password)
                if user:
                    user.password = hash_password
                    session.commit()
                db_user = DB_User.User(
                    email=user.email,
                    fname=user.fname,
                    lname=user.lname,
                    is_active=user.is_active
                )
                return db_user
        except Exception:
            raise HTTPException(status_code=400, detail=f"Error while updating the user please try again.")

    # Function for getting a list of users with pagination
    def get_users(skip: int, limit: int):
        try:
            with Session(engine) as session:
                db_user = session.query(DB_User.User).offset(skip).limit(limit).all()
                return db_user
        except Exception:
            raise HTTPException(status_code=400, detail=f"Error while getting users from database please try again.")

    # Function for getting a user by their email
    def get_user_by_email(email: str):
        try:
            with Session(engine) as session:
                db_user = session.query(DB_User.User).filter(DB_User.User.email == email).options(joinedload(DB_User.User.roles)).first()
                user = auth_models.UserRoles(
                    email=db_user.email,
                    fname=db_user.fname,
                    lname=db_user.lname,
                    id=db_user.id,
                    password=db_user.password,
                    is_active=db_user.is_active
                )
                for roles in db_user.roles:
                    user.roles.append(roles.name)
                return user
        except Exception:
            raise HTTPException(status_code=400, detail=f"Email does not exist.")
