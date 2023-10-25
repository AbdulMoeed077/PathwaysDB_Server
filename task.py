# from datetime import datetime, timedelta
# from fastapi import FastAPI, Query, Body, Cookie, Header, Form, File, UploadFile, HTTPException, Request, Depends, status
# from fastapi.responses import JSONResponse, PlainTextResponse
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from fastapi.exceptions import RequestValidationError
# from pydantic import BaseModel, Field, HttpUrl, EmailStr
# from typing import List, Literal
# from passlib.context import CryptContext
# from jose import jwt, JWTError
# app = FastAPI()

# # # list = []
# # # listLen = 0

# # # @app.post("/add")
# # # async def add_student(name : str, rollNo : str):
# # #     listLen = len(list) + 1
# # #     list.append([listLen, name, rollNo])
# # #     return list

# # # @app.get("/")
# # # async def display_all_student():
# # #     return list

# # # @app.get("/searchByID")
# # # async def search_by_id(stID: int):
# # #     for x in list:
# # #         print(x[0])
# # #         if(x[0] == stID):
# # #             return list[stID - 1]

# # # @app.get("/searchByName")
# # # async def search_by_name(stName: str):
# # #     for x in list:
# # #         print(x[1])
# # #         if(x[1] == stName):
# # #             return list[x[0] - 1]

# # # @app.get("/task1")
# # # async def data(q : int | None = Query(None, gt = 3)):
# # #     if q:
# # #         return {"task1": {("Task1: foo", "task2: bar")}}
# # #     else:
# # #         return {" ": "q"}

# # # class Item(BaseModel):
# # #     type: str
# # #     description: str | None = Field(None, title="The description of the item", max_length=300)

# # # @app.put("/itemss/{items_id}")
# # # async def update_item(item_id: int, item: Item = Body(..., embed=True)):
# # #     results = {"item_id": item_id, "item": item}
# # #     return results

# # # class Image(BaseModel):
# # #     url: HttpUrl
# # #     number: int
# # #     item: Item | None = None

# # # class Nested(BaseModel):
# # #     name: str
# # #     description: str | None = None
# # #     price: float
# # #     tags: List[int] = []
# # #     image: List[Image] | None = None 



# # # @app.put("/nested/{nested_id}")
# # # async def nested_item(nested_id: int, nested: Nested = Body(..., embed=True)):
# # #     results = {"item_id": nested_id, "item": nested}
# # #     return results

# # # @app.get("/cook")
# # # async def cookies(
# # #     cookie_id: str |None = Cookie(None),
# # #     accept_encoding: str | None = Header(None),
# # #     user_agent: str | None = Header(None),
# # #     sec_ch_ua: str | None = Header(None),
# # #     x_token: str | None = Header(None), 
# # # ):
# # #     return{
# # #         "cookie_id": cookie_id,
# # #         "Accept_Encoding": accept_encoding,
# # #         "User_Agent": user_agent,
# # #         "sec_ch_ua": sec_ch_ua,
# # #         "X_Token": x_token,
# # #     }

# # # class Schema_example(BaseModel):
# # #     userName: str 
# # #     description: str | None = None
# # #     price: int 
# # #     tax: float = 10.5
# # # class UserIn(Schema_example):
# # #     password: str
# # # class UserOut(Schema_example):
# # #     pass

# # # item={
# # #     "foo":{"userName": "foo", "price": 50},
# # #     "bar":{"userName": "bar", "description": "This is Bar", "price": 60, "tax": 10.5},
# # # }

# # # @app.post("/schema/", response_model=UserOut)
# # # async def responseModel(schema: UserIn):
# # #     return schema

# # # @app.get("/item/{schema}", response_model=Schema_example, response_model_exclude_unset=True, status_code=302)
# # # async def literalModel(schema: Literal["foo", "bar"]):
# # #     return item[schema]

# # # @app.post("/login")
# # # async def login(username: str = Form(...), password: str = Form(...)):
# # #     print("password", password)
# # #     return {"username", username}

# # # @app.post("/file")
# # # async def login(file:  UploadFile = File(...)):
# # #     content = await file.read()
# # #     return {"File Name": file.filename, "Content": content}

# # # @app.post("/files")
# # # async def login(files:  List[UploadFile] = File(...)):
# # #     return {"File Name": file.filename for file in files}


# # ##exception

# # # items = {"foo", "the foo is wrestler"}

# # # @app.get("/exception/")
# # # async def read_item(item_id: str):
# # #     if item_id not in items:
# # #         raise HTTPException(status_code=404, detail="Item not found", headers={"X-Errors": "Error due to wrong input"})
# # #     return {"item": items[item_id]}

# # # @app.exception_handler(RequestValidationError)
# # # async def validation_exception_handler(request, exc):
# # #     return PlainTextResponse(str(exc), status_code=418)

# # # @app.get("/validation_items/{item_id}")
# # # async def read_validation_items(item_id: int):
# # #     if item_id == 3:
# # #         raise HTTPException(status_code=418, detail="Node!")
# # #     return {"item_id": item_id}

# # #security
# # # oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# # # fake_users_db = {
# # #     "johndoe": dict(
# # #         username = "johndoe",
# # #         full_name = "John Doe",
# # #         email = "johndoe@example.com",
# # #         hashed_password = "fakehashedsecret",
# # #         disable = False
# # #     ),
# # #     "alice": dict(
# # #         username = "alice",
# # #         full_name = "Alice Wonderson",
# # #         email = "alice@example.com",
# # #         hashed_password = "fakehashedsecret2",
# # #         disable = True
# # #     )
# # # }

# # # def fake_hash_password(password: str):
# # #     return f"fakehashed{password}"

# # # class User(BaseModel):
# # #     username: str
# # #     email: str | None = None
# # #     full_name: str | None = None
# # #     disable: bool | None = None

# # # class UserInDb(User):
# # #     hashed_password: str

# # # def get_user(db, username: str):
# # #     if username in db:
# # #         user_dict = db[username]
# # #         return UserInDb(**user_dict)

# # # def fake_decode_token(token):
# # #     return get_user(fake_users_db, token)


# # # async def get_current_user(token: str = Depends(oauth2_scheme)):
# # #     user = fake_decode_token(token)
# # #     if not user:
# # #         raise HTTPException(
# # #             status_code=status.HTTP_401_UNAUTHORIZED,
# # #             detail="Invalid authentication credentials",
# # #             headers={"WWW-Authenticate": "Bearer"}
# # #         )
# # #     return user

# # # async def get_current_active_user(current_user: User = Depends(get_current_user)):
# # #     if current_user.disable:
# # #         raise HTTPException(status_code=400, detail="Inactive User")
# # #     return current_user

# # # @app.post("/token")
# # # async def login(form_data: OAuth2PasswordRequestForm = Depends()):
# # #     user_dict = fake_users_db.get(form_data.username)
# # #     if not user_dict:
# # #         raise HTTPException(
# # #             status_code=status.HTTP_401_UNAUTHORIZED,
# # #             detail="Incorrect username or password",
# # #         )
# # #     user = UserInDb(**user_dict)
# # #     hashed_password = fake_hash_password(form_data.password)
# # #     if not hashed_password == user.hashed_password:
# # #         raise HTTPException(status_code=400, detail="Inactive User")
    
# # #     return {"access_token": user.username, "token_type": "bearer" }

# # # @app.get("/users/me")
# # # async def get_me(current_user: User = Depends(get_current_active_user)):
# # #      return current_user

# # # @app.get("/items")
# # # async def read_items(token: str = Depends(oauth2_scheme)):
# # #     return {"token": token}

# #secret token with JWT

# SECRET_KEY="thequickbrownfoxjumpsoverthelazydog"
# ALOGRITHEM = 'HS256'
# ACCESS_TOKEN_MINUTES = 30

# fake_users_db = {
#     "johndoe": dict(
#         username = "johndoe",
#         full_name = "John Doe",
#         email = "johndoe@example.com",
#         hashed_password = "$2a$12$DO9oBwvz26zL3bEGu6XS7OY9tJI0uIOHveWgk4AqxkGdEF6UU9Dz.",
#         disable = False
#     ),
#     "alice": dict(
#         username = "alice",
#         full_name = "Alice Wonderson",
#         email = "alice@example.com",
#         hashed_password = "",
#         disable = True
#     )
# }

# class Token(BaseModel):
#     access_token: str
#     token_type: str

# class TokenData(BaseModel):
#     username:str | None = None

# class User(BaseModel):
#     username: str
#     email: str | None = None
#     full_name: str | None = None
#     disabled: bool = False

# class UserINDB(User):
#     hashed_password: str

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# def get_password_hash(password):
#     return pwd_context.hash(password)

# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         return UserINDB(**user_dict)

# def authenticate_user(fake_db, username: str, password: str):
#     user = get_user(fake_db, username)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user

# def create_access_token(data:dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes = 15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALOGRITHEM)
#     return encoded_jwt

# @app.post("/token", response_model=Token)
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = authenticate_user(fake_users_db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(status_code=400, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    
#     access_token_expires = timedelta(minutes = ACCESS_TOKEN_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta = access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}

# async def get_current_user(token:str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALOGRITHEM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
#     user = get_user(fake_users_db, username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user


# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive User")
#     return current_user

# @app.get("/users/me", response_model=User)
# async def get_me(current_user: User = Depends(get_current_active_user)):
#     return current_user

# @app.get("/users/me/items/")
# async def read_own_items(
#    current_user: User = Depends(get_current_active_user)
# ):
#     return [{"item_id": "Foo", "owner": current_user.username}]