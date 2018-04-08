import logging
import random

from django.shortcuts import render
from rest_framework import viewsets
from django.conf import settings
from rest_framework import exceptions, status
from django.core.mail import send_mail
from django.core.mail import EmailMessage 
from rest_framework.decorators import action
from django.contrib.auth import authenticate
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from rest_condition import And, Or, Not
from rest_framework.permissions import AllowAny
from django.http import Http404

from user_management.serializers import UsersSerializerCreate, \
                                        UsersSerializerList, \
                                        UsersSerializerUpdate
from user_management import strings
from user_management.models import Users
from user_management.custom_permission_classes import IsAuthenticated,IsListRequest, IsCreateRequest, IsRetrieveRequest, \
                        IsUpdateRequest, IsDeleteRequest, IsAdmin

log = logging.getLogger(__name__)
# Create your views here.


class UsersViewset(viewsets.ViewSet):

    permission_classes = [And(
                                Or(   And(IsListRequest,IsAuthenticated,IsAdmin),
                                      And(IsCreateRequest, AllowAny),
                                      And(IsRetrieveRequest,IsAuthenticated,),
                                      And(IsUpdateRequest,IsAuthenticated),
                                      And(IsDeleteRequest,IsAuthenticated,),
                                  )
                              )
                         ]

    def get_object(self,pk):
        '''
            Will fetch user object based on id.
            Will return Http404 if not found
        '''
        my_users = get_user_model()     
        try:
            return my_users.objects.get(pk=pk)
        except Exception as e:
            raise Http404

    def list(self,request,format=None): 
        '''
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
        '''
        queryset = Users.objects.all()
        serializer = UsersSerializerList(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, format=None):
        
        '''
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

        '''
        serializer = UsersSerializerCreate(data=request.data)
        if serializer.is_valid():
            serializer.save()
            try:
                #send mail
                username = request.data['username']
                usr_email = request.data['email']
                subject = "Account created"
                message = "Hi,\nYour account has been created successfully.\nusername: %s\n\nRegards,\nAdmin" %(username)
                mail_status = send_mail(subject,message, str(settings.EMAIL_HOST_USER),[usr_email])
            except Exception as e:
                log.error("error in sending mail: " + str(e))

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk, format=None):
        '''
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
                  
        '''
        designation = request.user.designation

        # Allowed for itself for staff
        if (designation == strings.STAFF):
            if not (pk == str(request.user.id)):
                raise exceptions.PermissionDenied(detail= strings.INVALID_CLIENT)   

        user = self.get_object(pk)
        try:
            serializer = UsersSerializerList(user)
            return Response(serializer.data)
        except Exception as e:
            log.error(strings.SERIALIZATION_ERROR_MSG)
            return Response(serializer.errors)

    def update(self, request, pk, format=None):

        '''
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
        '''

        if not (pk == str(request.user.id)):
            raise exceptions.PermissionDenied(detail= strings.INVALID_CLIENT)

        user = self.get_object(pk)
        data = request.data
        serializer = UsersSerializerUpdate(user, data=data)
        if serializer.is_valid():
            try:
                serializer.save()
            except Exception as e:
                res_msg = {'error': str(e)}
                log.error(res_msg)
                return Response(res_msg)
            return Response(serializer.data)
        log.error(serializer.errors)
        return Response(serializer.errors)

    def delete(self, request, pk, format=None):

        '''
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
        '''

        designation = request.user.designation

        # Allowed for itself for staff
        if (designation == strings.STAFF and pk != str(request.user.id)):            
            #Staff cannot delete anyone else account
            raise exceptions.PermissionDenied(detail= strings.INVALID_CLIENT)   
        if (designation == strings.ADMIN and pk == str(request.user.id)):
            #Even admin cannot delete admin account
            raise exceptions.PermissionDenied(detail= strings.CANNOT_DELETE_ADMIN)   

        user = self.get_object(pk)
        username = user.username
        usr_email = user.email        
        try:
            user.delete()
            res_msg = {"msg": strings.DATA_DELETED_SUCCESS}
            try:
                #send mail
                subject = "Account deleted"
                message = "Hi %s,\nYour account has been deleted successfully.\n\nRegards,\nAdmin" %(username)
                mail_status = send_mail(subject,message, str(settings.EMAIL_HOST_USER),[usr_email])
            except Exception as e:
                log.error("error in sending mail: " + str(e))            
            return Response(res_msg)
        except Exception as e:
            log.error(str(e))
            res_msg = {"error": str(e)}
            return Response(res_msg)

    @action(methods=['post'],detail = False ,permission_classes=[AllowAny,])
    def changepassword(self, request,format=None):
        '''
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
        '''     
        data = request.data

        username = data['username']
        old_password = data['old_password']
        new_password = data['new_password']
        try:
            my_user = authenticate(username=username, password=old_password)
            my_user.set_password(new_password)
            my_user.save()
            res_msg = {'msg': strings.PASSWORD_CHANGED_SUCCESSFULLY}

            try:
                #send mail
                username = request.data['username']
                usr_email = my_user.email
                subject = "Password changed"
                message = "Hi,\nYour account password has been changed successfully.\n\nRegards,\nAdmin"
                mail_status = send_mail(subject,message, str(settings.EMAIL_HOST_USER),[usr_email])
            except Exception as e:
                log.error("error in sending mail: " + str(e))

            return Response(res_msg)            
        except Exception as e:
            res_error = {'error': str(e)}
            log.error(str(res_error))
            return Response(res_error)

    @action(methods=['post'],detail = False ,permission_classes=[AllowAny,])
    def forgetpassword(self, request,format=None):
        '''
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
        '''             
        data = request.data
        username = data['username']
        try:
            my_users = get_user_model()
            my_user = my_users.objects.get(username = username)
            gen_pwd = str(random.randint(10000,99999)) # will generate 5 digit number ramdomly
            my_user.set_password(gen_pwd)
            my_user.save()
            res_msg = {'msg': strings.PASSWORD_RESETTED_SUCCESSFULLY}

            try:
                #send mail
                username = request.data['username']
                usr_email = my_user.email
                subject = "Password resetted"
                message = "Hi,\nKindly use OTP to login into your account.\nOTP: %s\n\nRegards,\nAdmin" %(gen_pwd)
                mail_status = send_mail(subject,message, str(settings.EMAIL_HOST_USER),[usr_email])
            except Exception as e:
                log.error("error in sending mail: " + str(e))

            return Response(res_msg)            
        except Exception as e:
            res_error = {'error': str(e)}
            log.error(str(res_error))
            return Response(res_error)

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated,])
    def get_user_details_from_token(self, request, format=None):
        '''
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
        '''
        log.info("Token Accepted!!!")        
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
            'firstname' : request.user.firstname,
            'lastname' : request.user.lastname,
            'email':  request.user.email,
            'id' : str(request.user.id),
            'designation' : str(request.user.designation)
        }
        return Response(content)    
      
