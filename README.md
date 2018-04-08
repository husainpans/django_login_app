
This is a user management application.
#######################################################################
Installation:
Requires python 2.7

# Create a virtualenv to isolate our package dependencies locally
virtualenv env
source env/bin/activate 

pip install Django==1.10
pip install django-rest-swagger==2.1.2
pip install djangorestframework==3.8.2
pip install djangorestframework-jwt==1.11.0
pip install rest-condition==1.0.3

########################################################################
Run project:
python manage.py runserver <free-port>
(By default 8000 port will be used)
########################################################################
Users are of 2 designation:
1) ADMIN: Onlu one admin user is possible, which is there by default.
   username: admin
   password: admin
2) STAFF: As many staff users can be created. 
#######################################################################
DB: SQLITE
#######################################################################
Authentication: JWT authentication has been used to authenticate users
#######################################################################
EMAIL configuration:

User management application is configured to send mails. So user first we need to configure email ID and password. It must be office365 account. This account will be used to send mails. 

To configure mail account update following 2 fields under django_login_proj/settings.py file.

EMAIL_HOST_USER = 'enter your office365 email ID'
EMAIL_HOST_PASSWORD = 'enter your password'

#######################################################################
API's:

1) Login:
API: /login
Request type: POST
Request Data:
    {
        "username":"string",
        "password": "string"        
    }
Response data:
    {
        "token": "string"
    }   

user need to provide this token in accessing other API's.    

2) List of users:
It will return list of Users. 
Only admin can access this API.        

API: /users/
Request type: GET

Headers: 
    Authorization: JWT <token>

Response data:
    [
        {
            "id": int,
            "username": "string",
            "email": "string",
            "firstname": "string",
            "lastname": "string",
            "designation": "string"
        }
    ]

3) Create User:
It will create new user. User will get email notification.
API: /users/
Request type: POST

Request data:
   {
        "username": "string",
        "email": "string",
        "firstname": "string",
        "lastname": "string",
        "password" : "string"
    }

Response data:
    {
        "id": int,
        "password": "string",
        "username": "string",
        "email": "string",
        "firstname": "string",
        "lastname": "string"
    }  

4) Retrieve user details:
It will return specific user data.
ADMIN can retrieve any account. STAFF can retrieve itself only.

API: /users/id/
Request type: GET

Headers: 
    Authorization: JWT <token>

Response data:

        {
            "id": int,
            "username": "string",
            "email": "string",
            "firstname": "string",
            "lastname": "string",
            "designation": "string"
        }    

5) Update user:
It will return specific user data.
User can update details of itself only

API: /users/id/
Request type: GET

Headers: 
    Authorization: JWT <token>

Request data:

        {
            "email": "string",
            "firstname": "string",
            "lastname": "string",
        }
          
Response data:

        {
            "email": "string",
            "firstname": "string",
            "lastname": "string",
        }  

6) Delete User:
It will return specific user data. Notification will be sent to user over its email ID.
ADMIN can delete any account. STAFF can delete itself only.
API: /users/id/
Request type: DELETE

Headers: 
    Authorization: JWT <token>

Response data:        
    {
        "msg": "Data deleted successfully"
    }  

7) Change Password:
It will change password of user and send notification over user email ID.
API: /users/changepassword/
Request type: POST

Request data:

        {
            "username": "string",
            "old_password": "string",
            "new_password": "string",
        }
          
Response data:

    {
        "msg":"Password changed successfully."
    }             

8) Forget Password:
It will reset users password and will mail OTP to user email ID.
API: /users/forgetpassword/
Request type: POST

Request data:

        {
            "username": "string"
        }
          
Response data:

    {
        "msg":"Password resetted successfully."
    }     

9) Get user details from token
It will return user details based from its token
API: /users/get_user_details_from_token/
Request type: GET
          
Headers: 
    Authorization: JWT <token>

Response data:

    {
        "designation": "string",
        "firstname": "string",
        "lastname": "string",
        "auth": "token string",
        "email": "string",
        "user": "string",
        "id": "string"
    }      
10) Swagger link:  http://<IP>/#/
    (Swagger document is remaining)
#######################################################################    